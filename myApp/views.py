from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Prefetch

from django.views.decorators.clickjacking import xframe_options_exempt

from django.contrib.messages import get_messages

from .models import (
    QuoteRequest,
    Profile,
    AdminAbout,
    AboutHero,
    TimelineEvent,
    TeamMember,
    CoreValue,
    ServiceCategory,
    ServiceItem,
    ServicesHero,
    ContactDetail,
    WorkExperience,
    Education,
    Attachment,
    QualificationDocument,
    JobPost,
    JobApplication,
    JobPostContent,
    CareersMainTopics,
    ContactHero,
    MainTopicBox,
    TopicDescription,
    HomeHero,
    HomeAbout,
    HomeServices,
    HomeServiceItem,
    HomeWhy,
    HomeWhyItem,
    SiteHeader,
    Footer,
    FooterServiceItem,
    FooterContactItem,
    EmailVerification,
    PasswordReset,
    CustomUser,
    HeroPhoto,
)

from .services.email_service import (
    send_verification_email,
    send_new_signup_admin_email,
    send_welcome_email,
    send_password_reset_email,
    send_password_changed_email,
)

User = get_user_model()

def clear_messages(request):
    storage = get_messages(request)
    for message in storage:
        pass


# =====================================================
# 1. AUTHENTICATION - SIGNUP
# =====================================================

def signup(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "myApp/signup.html")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already in use")
            return render(request, "myApp/signup.html")

        try:
            # Create user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=firstname,
                last_name=lastname,
                usercategory='customer',
                is_active=False
            )

            # Create verification record
            verification = EmailVerification.objects.create(
                user=user
            )

            # Send verification email to user
            send_verification_email(
                user=user,
                token=verification.token,
                request=request
            )

            # Notify admin about new signup
            try:
                send_new_signup_admin_email(user)
            except Exception as e:
                print("🔥 ADMIN NOTIFICATION ERROR:", e)

            # Force resend verification section on signin page
            request.session['just_signed_up'] = True
            request.session['pending_verification_email'] = email

        except Exception as e:
            messages.error(
                request,
                f"Error creating user: {e}"
            )
            return render(
                request,
                "myApp/signup.html"
            )
        
        clear_messages(request)

        messages.success(
            request,
            "Verification email sent. Please check your email to activate your account."
        )

        return redirect('signin')

    return render(
        request,
        "myApp/signup.html"
    )


# =====================================================
# 2. AUTHENTICATION - SIGNIN
# =====================================================

def signin(request):

    if not request.session.get('just_signed_up'):
        clear_messages(request)

    show_resend = False
    pending_email = None

    # 🔥 SHOW RESEND AFTER SIGNUP
    if request.session.get('just_signed_up'):
        show_resend = True
        pending_email = request.session.get('pending_verification_email')
        request.session.pop('just_signed_up', None)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next") or request.GET.get("next")

        # -------------------------------------------------
        # Check whether the account exists first
        # -------------------------------------------------

        existing_user = User.objects.filter(username=username).first()

        if existing_user:

            # Account exists but email has not been verified
            if not existing_user.is_active:

                show_resend = True
                pending_email = existing_user.email

                clear_messages(request)

                messages.warning(
                    request,
                    "You have not verified your account yet. "
                    "Please check your email, or request another verification email below."
                )

                return render(
                    request,
                    "myApp/signin.html",
                    {
                        "show_resend": show_resend,
                        "pending_email": pending_email,
                        "next": next_url or "",
                    },
                )

        # -------------------------------------------------
        # Normal authentication
        # -------------------------------------------------

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if not user:

            clear_messages(request)

            messages.error(
                request,
                "Invalid username or password."
            )

            return redirect("signin")

        # 🔐 LOGIN USER
        login(request, user)

        clear_messages(request)

        messages.success(
            request,
            "You signed in successfully."
        )

        # 🧠 clear pending signup session
        request.session.pop('pending_verification_email', None)

        category = (user.usercategory or "").strip().lower()

        # -----------------------------
        # CUSTOMER
        # -----------------------------
        if category == "customer":
            return redirect(next_url if next_url else 'home')

        # -----------------------------
        # ADMIN
        # -----------------------------
        elif category == "admin":
            request.session['frontend_admin_id'] = user.id
            return redirect(next_url if next_url else 'admindashboard')

        # -----------------------------
        # HR
        # -----------------------------
        elif category == "hr":
            request.session['frontend_hr_id'] = user.id
            return redirect(next_url if next_url else 'hrdashboard')

        # -----------------------------
        # UNKNOWN ROLE
        # -----------------------------
        clear_messages(request)

        messages.error(request, "Access denied. Invalid user role.")
        return redirect('signin')

    return render(request, "myApp/signin.html", {
        "show_resend": show_resend,
        "pending_email": pending_email,
        "next": request.GET.get('next', '')
    })


# =====================================================
# 3. AUTHENTICATION - SIGNOUT
# =====================================================

def signout(request):

    if 'frontend_admin_id' in request.session:
        request.session.flush()
        messages.success(
            request,
            "You have been signed out successfully."
        )
        return redirect('home')

    logout(request)

    messages.success(
        request,
        "You have been signed out successfully."
    )

    return redirect('home')


# =====================================================
# 4. AUTHENTICATION - EMAIL VERIFICATION
# =====================================================

def verify_email(request, token):
    try:
        verification = EmailVerification.objects.get(token=token)

        # check if already verified
        if verification.is_verified:
            messages.info(request, "Account already verified. Please sign in.")
            return redirect('signin')

        # check expiry
        if verification.expires_at < timezone.now():
            messages.error(request, "Verification link expired.")
            return redirect('signin')

        # activate user
        user = verification.user
        user.is_active = True
        user.save()

        # mark verification as done
        verification.is_verified = True
        verification.save()

        # 🎉 SEND WELCOME EMAIL (NEW STEP)
        send_welcome_email(user)

        messages.success(request, "Email verified successfully. You can now sign in.")
        return redirect('signin')

    except EmailVerification.DoesNotExist:
        messages.error(request, "Invalid verification link.")
        return redirect('signin')


def resend_verification_email(request):
    if request.method != "POST":
        return redirect("signin")

    email = request.POST.get("email")

    try:
        user = User.objects.get(email=email)

        # 🚨 If already verified
        if user.is_active:
            messages.info(request, "Account already verified. Please sign in.")
            return redirect("signin")

        # ✅ Get existing verification OR create new ONE properly
        verification, created = EmailVerification.objects.get_or_create(
            user=user
        )

        # 🔥 CRITICAL FIX:
        # If token is missing OR invalid, regenerate properly
        if not verification.token:
            verification.save()  # triggers UUID auto-generation

        # 🔥 FORCE SAVE (ensures UUID is valid in DB)
        verification.refresh_from_db()

        # 📧 SEND EMAIL AGAIN (ALWAYS WORKS)
        send_verification_email(
            user=user,
            token=str(verification.token),
            request=request
        )

        messages.success(request, "Verification email sent again. Please check your inbox.")
        return redirect("signin")

    except User.DoesNotExist:
        messages.error(request, "No account found with this email.")
        return redirect("signin")


# =====================================================
# 5. AUTHENTICATION - PASSWORD RESET
# =====================================================

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)

            reset = PasswordReset.objects.create(
                user=user
            )

            send_password_reset_email(
                user=user,
                token=reset.token,
                request=request
            )

            messages.success(
                request,
                "Password reset link sent to your email."
            )

            return redirect("signin")

        except User.DoesNotExist:
            messages.error(
                request,
                "No account found with that email."
            )

    return render(
        request,
        "myApp/forgot_password.html"
    )


def reset_password(request, token):
    try:
        reset = PasswordReset.objects.get(token=token)

        # ❌ already used
        if reset.is_used:
            messages.error(
                request,
                "This reset link has already been used."
            )
            return redirect("signin")

        # ❌ expired
        if reset.expires_at < timezone.now():
            messages.error(
                request,
                "Reset link has expired."
            )
            return redirect("signin")

        # ✅ handle password update
        if request.method == "POST":
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if password != confirm_password:
                messages.error(
                    request,
                    "Passwords do not match."
                )

                return render(
                    request,
                    "myApp/reset_password.html",
                    {"token": token}
                )

            user = reset.user

            # 🔐 update password
            user.set_password(password)
            user.save()

            # mark reset as used
            reset.is_used = True
            reset.save()

            # 📧 send confirmation email (IMPORTANT ADDITION)
            try:
                send_password_changed_email(user)
            except Exception as e:
                # don't break flow if email fails
                print("EMAIL ERROR:", e)

            messages.success(
                request,
                "Password changed successfully. Please sign in."
            )

            return redirect("signin")

        return render(
            request,
            "myApp/reset_password.html",
            {"token": token}
        )

    except PasswordReset.DoesNotExist:
        messages.error(
            request,
            "Invalid reset link."
        )
        return redirect("signin")


# =====================================================
# 7. ADMIN DASHBOARD
# =====================================================

def admindashboard(request):
    frontend_admin_id = request.session.get('frontend_admin_id')

    if not frontend_admin_id:
        return redirect('signin')

    admin_user = User.objects.filter(
        id=frontend_admin_id,
        usercategory='admin'
    ).first()

    if not admin_user:
        request.session.flush()
        return redirect('signin')

    return render(request, 'myApp/admindashboard.html', {
        'admin_user': admin_user
    })


def adminusers(request):
    users = User.objects.all().order_by('-id')  # newest first
    return render(request, "myApp/adminusers.html", {
        "users": users
    })


def adminherophotos(request):
    pages = ["home", "about", "services", "careers", "contact"]

    for p in pages:
        HeroPhoto.objects.get_or_create(page=p)

    hero_photos = HeroPhoto.objects.all()

    if request.method == "POST":
        page = request.POST.get("page")
        hero = HeroPhoto.objects.get(page=page)

        if "update_image" in request.POST:
            if request.FILES.get("image"):
                hero.image = request.FILES["image"]
                hero.save()

        if "delete_image" in request.POST:
            hero.image.delete(save=False)
            hero.image = None
            hero.save()

        return redirect("adminherophotos")

    return render(request, "myApp/adminherophotos.html", {
        "hero_photos": hero_photos
    })


# =====================================================
# 8. ADMIN - HEADER & FOOTER
# =====================================================

def adminheader(request):
    header, _ = SiteHeader.objects.get_or_create(id=1)

    if request.method == "POST":
        if "update_header" in request.POST:
            header.company_name = request.POST.get("company_name")
            if request.FILES.get("logo"):
                header.logo = request.FILES["logo"]
            header.save()
            return redirect("adminheader")

    return render(request, "myApp/adminheader.html", {
        "header": header
    })


def adminfooter(request):
    # ================= FOOTER MAIN =================
    footer, _ = Footer.objects.get_or_create(id=1)

    # ================= ITEMS =================
    service_items = FooterServiceItem.objects.all().order_by("id")
    contact_items = FooterContactItem.objects.all().order_by("id")

    if request.method == "POST":
        # ================= UPDATE FOOTER MAIN =================
        if "update_footer_main" in request.POST:
            footer.company_name = request.POST.get("company_name")
            footer.description = request.POST.get("description")
            footer.save()
            return redirect("adminfooter")

        # ================= SERVICE ITEMS =================
        if "add_service_item" in request.POST:
            FooterServiceItem.objects.create(
                title=request.POST.get("service_title"),
                description=request.POST.get("service_desc")
            )
            return redirect("adminfooter")

        if request.POST.get("delete_service_item"):
            FooterServiceItem.objects.filter(
                id=request.POST.get("delete_service_item")
            ).delete()
            return redirect("adminfooter")

        if "edit_service_item" in request.POST:
            item = FooterServiceItem.objects.get(id=request.POST.get("id"))
            item.title = request.POST.get("service_title")
            item.description = request.POST.get("service_desc")
            item.save()
            return redirect("adminfooter")

        # ================= CONTACT ITEMS =================
        if "add_contact_item" in request.POST:
            FooterContactItem.objects.create(
                title=request.POST.get("contact_title"),
                description=request.POST.get("contact_value"),
                link=request.POST.get("contact_link")
            )
            return redirect("adminfooter")

        if request.POST.get("delete_contact_item"):
            FooterContactItem.objects.filter(
                id=request.POST.get("delete_contact_item")
            ).delete()
            return redirect("adminfooter")

        if "edit_contact_item" in request.POST:
            item = FooterContactItem.objects.get(id=request.POST.get("id"))
            item.title = request.POST.get("contact_title")
            item.description = request.POST.get("contact_value")
            item.link = request.POST.get("contact_link")
            item.save()
            return redirect("adminfooter")

    return render(request, "myApp/adminfooter.html", {
        "footer": footer,
        "service_items": service_items,
        "contact_items": contact_items
    })


# =====================================================
# 9. ADMIN - HOME PAGE
# =====================================================

def adminhome(request):
    # ================= HERO =================
    homehero, _ = HomeHero.objects.get_or_create(id=1)

    # ================= ABOUT =================
    homeabout, _ = HomeAbout.objects.get_or_create(id=1)

    # ================= SERVICES =================
    homeservices, _ = HomeServices.objects.get_or_create(id=1)
    service_items = HomeServiceItem.objects.all().order_by("order", "id")

    # ================= WHY =================
    homewhy, _ = HomeWhy.objects.get_or_create(id=1)
    why_items = HomeWhyItem.objects.all().order_by("order", "id")

    if request.method == "POST":
        # ---------- HERO ----------
        if "update_homehero" in request.POST:
            homehero.title = request.POST.get("title")
            homehero.subtitle = request.POST.get("subtitle")
            homehero.coverage = request.POST.get("coverage")
            homehero.save()
            return redirect("adminhome")

        # ---------- ABOUT ----------
        if "update_homeabout" in request.POST:
            homeabout.title = request.POST.get("title")
            homeabout.subtitle = request.POST.get("subtitle")
            homeabout.paragraph1 = request.POST.get("paragraph1")
            homeabout.paragraph2 = request.POST.get("paragraph2")
            homeabout.years = request.POST.get("years")
            homeabout.vehicles = request.POST.get("vehicles")
            homeabout.deliveries = request.POST.get("deliveries")

            if request.FILES.get("image"):
                homeabout.image = request.FILES["image"]

            homeabout.save()
            return redirect("adminhome")

        # ---------- SERVICES ----------
        if "update_homeservices" in request.POST:
            homeservices.section_title = request.POST.get("section_title")
            homeservices.section_subtitle = request.POST.get("section_subtitle")
            homeservices.save()
            return redirect("adminhome")

        # ADD
        if "add_service_item" in request.POST:
            order = HomeServiceItem.objects.count()
            HomeServiceItem.objects.create(
                icon=request.POST.get("icon"),
                title=request.POST.get("item_title"),
                description=request.POST.get("item_desc"),
                order=order
            )
            return redirect("adminhome")

        # DELETE
        if request.POST.get("delete_service_item"):
            HomeServiceItem.objects.filter(
                id=request.POST.get("delete_service_item")
            ).delete()
            return redirect("adminhome")

        # EDIT
        if request.POST.get("edit_service_item"):
            item = HomeServiceItem.objects.get(
                id=request.POST.get("edit_service_item")
            )
            item.icon = request.POST.get("icon")
            item.title = request.POST.get("item_title")
            item.description = request.POST.get("item_desc")
            item.save()
            return redirect("adminhome")

        # ---------- WHY ----------
        if "update_homewhy" in request.POST:
            homewhy.section_title = request.POST.get("why_title")
            homewhy.section_subtitle = request.POST.get("why_subtitle")
            homewhy.save()
            return redirect("adminhome")

        # ADD
        if "add_why_item" in request.POST:
            order = HomeWhyItem.objects.count()
            HomeWhyItem.objects.create(
                icon=request.POST.get("why_icon"),
                title=request.POST.get("why_item_title"),
                description=request.POST.get("why_item_desc"),
                order=order
            )
            return redirect("adminhome")

        # DELETE
        if request.POST.get("delete_why_item"):
            HomeWhyItem.objects.filter(
                id=request.POST.get("delete_why_item")
            ).delete()
            return redirect("adminhome")

        # EDIT
        if request.POST.get("edit_why_item"):
            item = HomeWhyItem.objects.get(
                id=request.POST.get("edit_why_item")
            )
            item.icon = request.POST.get("why_icon")
            item.title = request.POST.get("why_item_title")
            item.description = request.POST.get("why_item_desc")
            item.save()
            return redirect("adminhome")

    return render(request, "myApp/adminhome.html", {
        "homehero": homehero,
        "homeabout": homeabout,
        "homeservices": homeservices,
        "service_items": service_items,
        "homewhy": homewhy,
        "why_items": why_items
    })


# =====================================================
# 10. ADMIN - ABOUT PAGE
# =====================================================

def adminabout(request):
    admin_id = request.session.get('frontend_admin_id')
    if not admin_id:
        return redirect('signin')

    about, created = AdminAbout.objects.get_or_create(id=1)
    hero = AboutHero.objects.filter(id=1).first()

    timeline = TimelineEvent.objects.all().order_by('year')
    team = TeamMember.objects.all()
    core_values = CoreValue.objects.all().order_by('order')

    if request.method == "POST":
        # ================= HERO UPDATE =================
        if "update_hero" in request.POST:
            hero, created = AboutHero.objects.get_or_create(id=1)
            hero.tagline = request.POST.get("tagline")
            hero.hero_title = request.POST.get("hero_title")
            hero.save()
            return redirect('adminabout')

        # ================= ABOUT CONTENT =================
        if "save_about" in request.POST:
            about.history_title = request.POST.get("history_title")
            about.history_subtitle = request.POST.get("history_subtitle")
            about.history_p1 = request.POST.get("history_p1")
            about.history_p2 = request.POST.get("history_p2")
            about.history_p3 = request.POST.get("history_p3")
            about.save()
            return redirect('adminabout')

        # ================= MISSION =================
        if "save_mission" in request.POST:
            about.mission = request.POST.get("mission")
            about.vision = request.POST.get("vision")
            about.save()
            return redirect('adminabout')

        # ================= TIMELINE ADD =================
        if "add_timeline" in request.POST:
            TimelineEvent.objects.create(
                year=request.POST.get("timeline_year"),
                description=request.POST.get("timeline_desc"),
                order=0
            )
            return redirect('adminabout')

        if "edit_timeline" in request.POST:
            event = TimelineEvent.objects.get(id=request.POST.get("edit_timeline_id"))
            event.year = request.POST.get("timeline_year")
            event.description = request.POST.get("timeline_desc")
            event.save()
            return redirect('adminabout')

        if "delete_timeline" in request.POST:
            TimelineEvent.objects.get(id=request.POST.get("delete_timeline_id")).delete()
            return redirect('adminabout')

        # ================= TEAM ADD =================
        if "add_team_member" in request.POST:
            TeamMember.objects.create(
                name=request.POST.get("team_name"),
                role=request.POST.get("team_role"),
                bio=request.POST.get("team_bio"),
                photo=request.FILES.get("team_photo")
            )
            return redirect('adminabout')

        if "edit_team_member" in request.POST:
            member = TeamMember.objects.get(id=request.POST.get("edit_team_member_id"))
            member.name = request.POST.get("team_name")
            member.role = request.POST.get("team_role")
            member.bio = request.POST.get("team_bio")

            if request.FILES.get("team_photo"):
                member.photo = request.FILES.get("team_photo")

            member.save()
            return redirect('adminabout')

        if "delete_team_member" in request.POST:
            TeamMember.objects.get(id=request.POST.get("delete_team_member_id")).delete()
            return redirect('adminabout')

        # ================= CORE VALUES =================
        if "save_values" in request.POST:
            titles = request.POST.getlist("value_title")
            descs = request.POST.getlist("value_desc")

            CoreValue.objects.all().delete()

            for i in range(len(titles)):
                if titles[i] or descs[i]:
                    CoreValue.objects.create(
                        title=titles[i],
                        description=descs[i],
                        order=i
                    )

            return redirect('adminabout')

    return render(request, "myApp/adminabout.html", {
        "about": about,
        "hero": hero,
        "timeline": timeline,
        "team": team,
        "core_values": core_values
    })


# =====================================================
# 11. ADMIN - SERVICES PAGE
# =====================================================

def adminservices(request):
    # ================= HERO =================
    hero, created = ServicesHero.objects.get_or_create(id=1)

    # ================= FETCH DATA =================
    categories = ServiceCategory.objects.all().prefetch_related("items")
    quotes = QuoteRequest.objects.all().order_by("-created_at")

    # ================= POST HANDLING =================
    if request.method == "POST":
        # ---------- UPDATE HERO ----------
        if "update_hero" in request.POST:
            hero, created = ServicesHero.objects.get_or_create(id=1)
            hero.tagline = request.POST.get("tagline")
            hero.hero_title = request.POST.get("hero_title")
            hero.save()
            return redirect("adminservices")

        # ---------- ADD CATEGORY ----------
        if "add_category" in request.POST:
            title = request.POST.get("category_title")
            if title:
                ServiceCategory.objects.create(title=title)
            return redirect("adminservices")

        # ---------- EDIT CATEGORY ----------
        if "edit_category" in request.POST:
            category_id = request.POST.get("category_id")
            new_title = request.POST.get("edit_category_title")

            if category_id and new_title:
                category = get_object_or_404(ServiceCategory, id=category_id)
                category.title = new_title
                category.save()

            return redirect("adminservices")

        # ---------- DELETE CATEGORY ----------
        if "delete_category" in request.POST:
            category_id = request.POST.get("delete_category_id")

            if category_id:
                category = get_object_or_404(ServiceCategory, id=category_id)
                category.delete()

            return redirect("adminservices")

        # ---------- ADD ITEM ----------
        if "add_item" in request.POST:
            category_id = request.POST.get("category_id")
            title = request.POST.get("item_title")
            desc = request.POST.get("item_desc")
            icon = request.POST.get("item_icon")

            if category_id and title and desc:
                category = get_object_or_404(ServiceCategory, id=category_id)
                ServiceItem.objects.create(
                    category=category,
                    title=title,
                    description=desc,
                    icon=icon
                )

            return redirect("adminservices")

        # ---------- EDIT ITEM ----------
        if "edit_item" in request.POST:
            item_id = request.POST.get("edit_item_id")

            if item_id:
                item = get_object_or_404(ServiceItem, id=item_id)
                item.title = request.POST.get("item_title")
                item.description = request.POST.get("item_desc")
                item.icon = request.POST.get("item_icon")
                item.save()

            return redirect("adminservices")

        # ---------- DELETE ITEM ----------
        if "delete_item" in request.POST:
            item_id = request.POST.get("delete_item_id")

            if item_id:
                item = get_object_or_404(ServiceItem, id=item_id)
                item.delete()

            return redirect("adminservices")

    # ================= RENDER =================
    return render(request, "myApp/adminservices.html", {
        "categories": categories,
        "quotes": quotes,
        "hero": hero
    })


# =====================================================
# 12. ADMIN - CAREERS PAGE
# =====================================================

def admincareers(request):
    jobs = JobPost.objects.all().order_by("-id")

    # =========================
    # CAREERS MAIN PAGE CONTENT
    # =========================
    careers_main, created = CareersMainTopics.objects.get_or_create(id=1)

    # =========================
    # EDIT MODE LOADERS
    # =========================
    edit_job = None
    edit_content = None

    if request.GET.get("edit_job"):
        edit_job = get_object_or_404(JobPost, id=request.GET.get("edit_job"))

    if request.GET.get("edit_content"):
        edit_content = get_object_or_404(JobPostContent, id=request.GET.get("edit_content"))

    # =========================
    # POST HANDLING
    # =========================
    if request.method == "POST":
        # =========================
        # UPDATE CAREERS MAIN PAGE
        # =========================
        if "update_careers_main" in request.POST:
            careers_main.tagline = request.POST.get("tagline")
            careers_main.hero_title = request.POST.get("hero_title")
            careers_main.intro_title = request.POST.get("intro_title")
            careers_main.intro_text = request.POST.get("intro_text")
            careers_main.open_positions_title = request.POST.get("open_positions_title")
            careers_main.save()

            messages.success(request, "Careers page updated successfully")
            return redirect("admincareers")

        # =========================
        # ADD JOB
        # =========================
        if "add_job" in request.POST:
            JobPost.objects.create(
                job_title=request.POST.get("job_title"),
                company_name=request.POST.get("company_name"),
                location=request.POST.get("location"),
                job_type=request.POST.get("job_type"),
                work_hours=request.POST.get("work_hours"),
                stipend=request.POST.get("stipend"),
                publish_date=request.POST.get("publish_date") or None,
                closing_date=request.POST.get("closing_date") or None,
            )

            messages.success(request, "Job added successfully")
            return redirect("admincareers")

        # =========================
        # UPDATE JOB
        # =========================
        if "update_job" in request.POST:
            job = get_object_or_404(JobPost, id=request.POST.get("edit_job_id"))
            job.job_title = request.POST.get("job_title")
            job.company_name = request.POST.get("company_name")
            job.location = request.POST.get("location")
            job.job_type = request.POST.get("job_type")
            job.work_hours = request.POST.get("work_hours")
            job.stipend = request.POST.get("stipend")
            job.publish_date = request.POST.get("publish_date") or None
            job.closing_date = request.POST.get("closing_date") or None
            job.save()

            messages.success(request, "Job updated successfully")
            return redirect("admincareers")

        # =========================
        # DELETE JOB
        # =========================
        if "delete_job_id" in request.POST:
            get_object_or_404(JobPost, id=request.POST.get("delete_job_id")).delete()
            messages.success(request, "Job deleted successfully")
            return redirect("admincareers")

        # =========================
        # ADD CONTENT
        # =========================
        if "add_content" in request.POST:
            job = get_object_or_404(JobPost, id=request.POST.get("job_id"))
            JobPostContent.objects.create(
                job=job,
                topic_title=request.POST.get("topic_title"),
                title_level=request.POST.get("title_level"),
                description=request.POST.get("description"),
                format_type=request.POST.get("format_type"),
            )

            messages.success(request, "Content added successfully")
            return redirect("admincareers")

        # =========================
        # UPDATE CONTENT
        # =========================
        if "update_content" in request.POST:
            content = get_object_or_404(JobPostContent, id=request.POST.get("edit_content_id"))
            content.job_id = request.POST.get("job_id")
            content.topic_title = request.POST.get("topic_title")
            content.title_level = request.POST.get("title_level")
            content.description = request.POST.get("description")
            content.format_type = request.POST.get("format_type")
            content.save()

            messages.success(request, "Content updated successfully")
            return redirect("admincareers")

        # =========================
        # DELETE CONTENT
        # =========================
        if "delete_content_id" in request.POST:
            get_object_or_404(JobPostContent, id=request.POST.get("delete_content_id")).delete()
            messages.success(request, "Content deleted successfully")
            return redirect("admincareers")

    return render(request, "myApp/admincareers.html", {
        "jobs": jobs,
        "careers_main": careers_main,
        "edit_job": edit_job,
        "edit_content": edit_content
    })


# =====================================================
# 13. ADMIN - CONTACT PAGE
# =====================================================

def admincontact(request):
    # ================= HERO =================
    hero, created = ContactHero.objects.get_or_create(id=1)

    # ================= BOXES =================
    contact_boxes = MainTopicBox.objects.all().prefetch_related("descriptions")

    # ================= POST HANDLING =================
    if request.method == "POST":
        # ---------- UPDATE HERO ----------
        if "update_hero" in request.POST:
            hero.tagline = request.POST.get("tagline")
            hero.hero_title = request.POST.get("hero_title")
            hero.save()
            return redirect("admincontact")

        # ---------- ADD BOX ----------
        if "add_box" in request.POST:
            MainTopicBox.objects.create(
                title=request.POST.get("box_title")
            )
            return redirect("admincontact")

        # ---------- ADD DESCRIPTION ----------
        if "add_paragraph" in request.POST:
            box = get_object_or_404(MainTopicBox, id=request.POST.get("box_id"))
            TopicDescription.objects.create(
                box=box,
                text=request.POST.get("text")
            )
            return redirect("admincontact")

        # ---------- DELETE BOX ----------
        if "delete_box_id" in request.POST:
            get_object_or_404(MainTopicBox, id=request.POST.get("delete_box_id")).delete()
            return redirect("admincontact")

        # ---------- DELETE DESCRIPTION ----------
        if "delete_item_id" in request.POST:
            get_object_or_404(TopicDescription, id=request.POST.get("delete_item_id")).delete()
            return redirect("admincontact")
        
        # ---------- EDIT BOX ----------
        if "edit_box" in request.POST:
            box = get_object_or_404(MainTopicBox, id=request.POST.get("box_id"))
            box.title = request.POST.get("edit_box_title")
            box.save()
            return redirect("admincontact")

        # ---------- EDIT ITEM ----------
        if "edit_item" in request.POST:
            item = get_object_or_404(TopicDescription, id=request.POST.get("item_id"))
            item.text = request.POST.get("edit_text")
            item.save()
            return redirect("admincontact")

    return render(request, "myApp/admincontact.html", {
        "hero": hero,
        "contact_boxes": contact_boxes
    })


# =====================================================
# 14. HR DASHBOARD
# =====================================================

@login_required
def hrdashboard(request):
    if request.user.usercategory != "hr":
        return redirect('home')

    return render(request, "myApp/hrdashboard.html")


def hrcareers(request):
    return render(request, "myApp/hrcareers.html")


# =====================================================
# 15. HR - APPLICANTS & APPLICATIONS
# =====================================================

@login_required
def hrapplicants(request):
    applicants = (
        CustomUser.objects
        .filter(jobapplication__isnull=False)
        .distinct()
        .annotate(application_count=Count("jobapplication"))
        .select_related("profile")
        .prefetch_related("jobapplication_set")
        .order_by("first_name", "last_name")
    )

    return render(
        request,
        "myApp/hrapplicants.html",
        {"applicants": applicants}
    )


@login_required
def hrapplicant_profile(request, user_id):
    applicant = get_object_or_404(CustomUser, id=user_id)
    profile = get_object_or_404(Profile, user=applicant)

    try:
        contact = ContactDetail.objects.get(profile=profile)
    except ContactDetail.DoesNotExist:
        contact = None

    work_experience = WorkExperience.objects.filter(profile=profile)
    education = Education.objects.filter(profile=profile)

    try:
        attachments = Attachment.objects.get(profile=profile)
    except Attachment.DoesNotExist:
        attachments = None

    qualification_documents = QualificationDocument.objects.filter(profile=profile)
    user_applications = JobApplication.objects.filter(user=applicant)

    return render(
        request,
        "myApp/hrapplicant_profile.html",
        {
            "applicant": applicant,
            "profile": profile,
            "contact": contact,
            "work_experience": work_experience,
            "education": education,
            "attachments": attachments,
            "qualification_documents": qualification_documents,
            "user_applications": user_applications,
        }
    )


@login_required
def hrapplications(request):
    applications = (
        JobApplication.objects
        .select_related("user", "job")
        .order_by("-date_applied")
    )

    return render(
        request,
        "myApp/hrapplications.html",
        {"applications": applications}
    )



def hrinterviews(request):
    return render(request, "myApp/hrinterviews.html")


def hroffers(request):
    return render(request, "myApp/hroffers.html")


def hrhired(request):
    return render(request, "myApp/hrhired.html")


def hrjobs(request):
    return render(request, "myApp/hrjobs.html")


def hrreports(request):
    return render(request, "myApp/hrreports.html")


# =====================================================
# 16. USER PROFILE - VIEW
# =====================================================

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    contact = ContactDetail.objects.filter(
        profile=profile
    ).first()

    work_experience = WorkExperience.objects.filter(
        profile=profile
    ).order_by("-start_date")

    education = Education.objects.filter(
        profile=profile
    ).order_by("-start_date")

    attachments = Attachment.objects.filter(
        profile=profile
    ).first()

    qualification_documents = (
        QualificationDocument.objects.filter(
            profile=profile
        ).order_by("-uploaded_at")
    )

    user_applications = JobApplication.objects.filter(
        user=request.user
    ).select_related(
        "job"
    ).order_by(
        "-id"
    )

    profile_alert = request.session.pop(
        "profile_alert",
        {
            "section": None,
            "message": "",
            "missing": []
        }
    )

    # Determine section to scroll to
    if profile_alert.get("section"):

        profile_alert["scroll_to"] = (
            profile_alert["section"] + "Section"
        )

    else:
        
        profile_alert["scroll_to"] = None
        
    missing = profile_alert.get("missing", [])

    profile_alert["is_missing"] = {

        # ============================================
        # PERSONAL DETAILS
        # ============================================
        "first_name": "first_name" in missing,
        "last_name": "last_name" in missing,
        "email": "email" in missing,
        "middle_name": "middle_name" in missing,
        "id_number": "id_number" in missing,
        "dob": "dob" in missing,
        "gender": "gender" in missing,
        "race": "race" in missing,
        "nationality": "nationality" in missing,
        "marital_status": "marital_status" in missing,
        "address": "address" in missing,
        "city": "city" in missing,
        "province": "province" in missing,
        "country": "country" in missing,

        # ============================================
        # CONTACT DETAILS
        # ============================================
        "contact_email": "email" in missing,
        "phone_primary": "phone_primary" in missing,

        # ============================================
        # DOCUMENTS
        # ============================================
        "resume": "resume" in missing,
        "id_document": "id_document" in missing,
    }

    return render(
        request,
        "myApp/profile.html",
        {
            "user": request.user,
            "profile": profile,
            "contact": contact,
            "work_experience": work_experience,
            "education": education,
            "attachments": attachments,
            "qualification_documents": qualification_documents,
            "user_applications": user_applications,
            "profile_alert": profile_alert,
        }
    )


# =====================================================
# 17. USER PROFILE - UPDATE
# =====================================================

@login_required
def update_profile(request):
    if request.method == "POST":
        user = request.user
        profile = user.profile
        form_type = request.POST.get("form_type")

        # ==========================================
        # PERSONAL DETAILS
        # ==========================================
        if form_type == "personal":
            # USER MODEL
            user.first_name = (
                request.POST.get("first_name")
                or user.first_name
            )
            user.last_name = (
                request.POST.get("last_name")
                or user.last_name
            )
            email = request.POST.get("email")
            if email:
                user.email = email
            user.save()

            # PROFILE MODEL
            profile_fields = [
                "middle_name",
                "id_number",
                "dob",
                "gender",
                "race",
                "nationality",
                "marital_status",
                # ADDRESS
                "address",
                "city",
                "province",
                "country",
            ]

            for field in profile_fields:
                value = request.POST.get(field)
                if value is not None:
                    if field == "dob":
                        setattr(
                            profile,
                            field,
                            value if value else None
                        )
                    else:
                        setattr(
                            profile,
                            field,
                            value.strip()
                        )
            profile.save()
            messages.success(
                request,
                "Personal details updated successfully."
            )
            return redirect("profile")

        # ==========================================
        # CONTACT DETAILS
        # ==========================================
        if form_type == "contact":
            contact, created = ContactDetail.objects.get_or_create(
                profile=profile
            )
            contact.email = (
                request.POST.get("contact_email")
                or ""
            )
            contact.phone_primary = (
                request.POST.get("phone_primary")
                or ""
            )
            contact.phone_alternative = (
                request.POST.get("phone_alternative")
                or ""
            )
            contact.linkedin = (
                request.POST.get("linkedin")
                or ""
            )
            contact.portfolio = (
                request.POST.get("portfolio")
                or ""
            )
            contact.save()
            messages.success(
                request,
                "Contact details updated successfully."
            )
            return redirect("profile")

        # ==========================================
        # WORK EXPERIENCE
        # ==========================================
        if form_type == "work":
            work_id = request.POST.get("work_id")
            currently_working = (
                request.POST.get("currently_working") == "on"
            )

            # UPDATE EXISTING RECORD
            if work_id:
                try:
                    work = WorkExperience.objects.get(
                        id=work_id,
                        profile=profile
                    )
                    work.company = (
                        request.POST.get("company")
                        or ""
                    )
                    work.job_title = (
                        request.POST.get("job_title")
                        or ""
                    )
                    work.description = (
                        request.POST.get("description")
                        or ""
                    )
                    work.start_date = (
                        request.POST.get("start_date")
                        or None
                    )
                    work.end_date = (
                        None
                        if currently_working
                        else (
                            request.POST.get("end_date")
                            or None
                        )
                    )
                    work.currently_working = (
                        currently_working
                    )
                    work.reason_for_leaving = (
                        request.POST.get("reason_for_leaving")
                        or ""
                    )
                    work.save()
                    messages.success(
                        request,
                        "Work experience updated successfully."
                    )
                except WorkExperience.DoesNotExist:
                    messages.error(
                        request,
                        "Work experience record not found."
                    )

            # CREATE NEW RECORD
            else:
                WorkExperience.objects.create(
                    profile=profile,
                    company=(
                        request.POST.get("company")
                        or ""
                    ),
                    job_title=(
                        request.POST.get("job_title")
                        or ""
                    ),
                    description=(
                        request.POST.get("description")
                        or ""
                    ),
                    start_date=(
                        request.POST.get("start_date")
                        or None
                    ),
                    end_date=(
                        None
                        if currently_working
                        else (
                            request.POST.get("end_date")
                            or None
                        )
                    ),
                    currently_working=currently_working,
                    reason_for_leaving=(
                        request.POST.get("reason_for_leaving")
                        or ""
                    ),
                )
                messages.success(
                    request,
                    "Work experience added successfully."
                )
            return redirect("profile")

        # ==========================================
        # EDUCATION
        # ==========================================
        if form_type == "education":
            education_id = request.POST.get(
                "education_id"
            )

            # UPDATE EXISTING RECORD
            if education_id:
                try:
                    education = Education.objects.get(
                        id=education_id,
                        profile=profile
                    )
                    education.school_name = (
                        request.POST.get("school_name")
                        or None
                    )
                    education.qualification = (
                        request.POST.get("qualification")
                        or None
                    )
                    education.qualification_level = (
                        request.POST.get("qualification_level")
                        or None
                    )
                    education.start_date = (
                        request.POST.get("start_date")
                        or None
                    )
                    education.end_date = (
                        request.POST.get("end_date")
                        or None
                    )
                    education.save()
                    messages.success(
                        request,
                        "Education updated successfully."
                    )
                except Education.DoesNotExist:
                    messages.error(
                        request,
                        "Education record not found."
                    )

            # CREATE NEW RECORD
            else:
                Education.objects.create(
                    profile=profile,
                    school_name=(
                        request.POST.get("school_name")
                        or None
                    ),
                    qualification=(
                        request.POST.get("qualification")
                        or None
                    ),
                    qualification_level=(
                        request.POST.get("qualification_level")
                        or None
                    ),
                    start_date=(
                        request.POST.get("start_date")
                        or None
                    ),
                    end_date=(
                        request.POST.get("end_date")
                        or None
                    ),
                )
                messages.success(
                    request,
                    "Education record added successfully."
                )
            return redirect("profile")

        # ==========================================
        # QUALIFICATION DOCUMENT
        # ==========================================
        if form_type == "qualification_document":
            qualification_id = request.POST.get(
                "qualification_id"
            )
            remove_certificate = (
                request.POST.get(
                    "remove_certificate"
                ) == "true"
            )

            # UPDATE EXISTING QUALIFICATION
            if qualification_id:
                try:
                    qualification = QualificationDocument.objects.get(
                        id=qualification_id,
                        profile=profile
                    )
                    qualification.qualification_name = (
                        request.POST.get(
                            "qualification_name"
                        )
                        or None
                    )
                    # REMOVE CURRENT CERTIFICATE
                    if remove_certificate:
                        if qualification.certificate:
                            qualification.certificate.delete(
                                save=False
                            )
                        qualification.certificate = None
                    # REPLACE CERTIFICATE
                    elif request.FILES.get(
                        "certificate"
                    ):
                        if qualification.certificate:
                            qualification.certificate.delete(
                                save=False
                            )
                        qualification.certificate = (
                            request.FILES.get(
                                "certificate"
                            )
                        )
                    qualification.save()
                    messages.success(
                        request,
                        "Qualification updated successfully."
                    )
                except QualificationDocument.DoesNotExist:
                    messages.error(
                        request,
                        "Qualification record not found."
                    )

            # CREATE NEW QUALIFICATION
            else:
                QualificationDocument.objects.create(
                    profile=profile,
                    qualification_name=(
                        request.POST.get(
                            "qualification_name"
                        )
                        or None
                    ),
                    certificate=(
                        request.FILES.get(
                            "certificate"
                        )
                    )
                )
                messages.success(
                    request,
                    "Qualification added successfully."
                )
            return redirect("profile")

        # ==========================================
        # ATTACHMENTS / SINGLE DOCUMENTS
        # ==========================================
        if form_type == "documents":
            attachments, created = Attachment.objects.get_or_create(
                profile=profile
            )

            # REMOVE DOCUMENTS
            remove_resume = (
                request.POST.get(
                    "remove_resume"
                ) == "true"
            )
            remove_id_document = (
                request.POST.get(
                    "remove_id_document"
                ) == "true"
            )
            remove_matric_certificate = (
                request.POST.get(
                    "remove_matric_certificate"
                ) == "true"
            )

            # REMOVE RESUME
            if remove_resume:
                if attachments.resume:
                    attachments.resume.delete(
                        save=False
                    )
                attachments.resume = None
            # UPDATE RESUME
            elif request.FILES.get("resume"):
                if attachments.resume:
                    attachments.resume.delete(
                        save=False
                    )
                attachments.resume = (
                    request.FILES.get("resume")
                )

            # REMOVE ID DOCUMENT
            if remove_id_document:
                if attachments.id_document:
                    attachments.id_document.delete(
                        save=False
                    )
                attachments.id_document = None
            # UPDATE ID DOCUMENT
            elif request.FILES.get("id_document"):
                if attachments.id_document:
                    attachments.id_document.delete(
                        save=False
                    )
                attachments.id_document = (
                    request.FILES.get("id_document")
                )

            # REMOVE MATRIC CERTIFICATE
            if remove_matric_certificate:
                if attachments.matric_certificate:
                    attachments.matric_certificate.delete(
                        save=False
                    )
                attachments.matric_certificate = None
            # UPDATE MATRIC CERTIFICATE
            elif request.FILES.get("matric_certificate"):
                if attachments.matric_certificate:
                    attachments.matric_certificate.delete(
                        save=False
                    )
                attachments.matric_certificate = (
                    request.FILES.get("matric_certificate")
                )

            attachments.save()
            messages.success(
                request,
                "Documents updated successfully."
            )
            return redirect("profile")
        
        return redirect("profile")


# =====================================================
# 18. USER PROFILE - DELETE
# =====================================================

@login_required
def delete_profile(request):
    if request.method == "POST":
        profile = request.user.profile
        delete_type = request.POST.get(
            "delete_type"
        )

        # ==========================================
        # WORK EXPERIENCE
        # ==========================================
        if delete_type == "work":
            work_id = request.POST.get(
                "work_id"
            )
            try:
                work = WorkExperience.objects.get(
                    id=work_id,
                    profile=profile
                )
                work.delete()
                messages.success(
                    request,
                    "Work experience deleted successfully."
                )
            except WorkExperience.DoesNotExist:
                messages.error(
                    request,
                    "Work experience not found."
                )

        # ==========================================
        # EDUCATION
        # ==========================================
        elif delete_type == "education":
            education_id = request.POST.get(
                "education_id"
            )
            try:
                education = Education.objects.get(
                    id=education_id,
                    profile=profile
                )
                education.delete()
                messages.success(
                    request,
                    "Education record deleted successfully."
                )
            except Education.DoesNotExist:
                messages.error(
                    request,
                    "Education record not found."
                )

        # ==========================================
        # QUALIFICATION DOCUMENT
        # ==========================================
        elif delete_type == "qualification_document":
            qualification_id = request.POST.get(
                "qualification_id"
            )
            try:
                qualification = QualificationDocument.objects.get(
                    id=qualification_id,
                    profile=profile
                )
                # Delete uploaded file from storage
                if qualification.certificate:
                    qualification.certificate.delete(
                        save=False
                    )
                qualification.delete()
                messages.success(
                    request,
                    "Qualification certificate deleted successfully."
                )
            except QualificationDocument.DoesNotExist:
                messages.error(
                    request,
                    "Qualification certificate not found."
                )

        return redirect("profile")

    return redirect("profile")


# =====================================================
# 19. USER - EXTRA PAGES (Notifications, Inbox, Settings, etc.)
# =====================================================

def notifications(request):
    return render(request, "myApp/notifications.html")


def inbox(request):
    return render(request, "myApp/inbox.html")


def settings(request):
    return render(request, "myApp/settings.html")


def feedback(request):
    return render(request, "myApp/feedback.html")


def help(request):
    return render(request, "myApp/help.html")


# =====================================================
# 20. JOB APPLICATION (User applies for job)
# =====================================================

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    user = request.user

    if user.usercategory != "customer":
        messages.error(
            request,
            "Only applicants can apply for jobs."
        )
        return redirect("jobinfo", job.id)

    profile = user.profile

    missing_sections = {}

    # ==================================================
    # PERSONAL DETAILS CHECK
    # ==================================================

    personal_missing = []

    personal_fields = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "middle_name": profile.middle_name,
        "id_number": profile.id_number,
        "dob": profile.dob,
        "gender": profile.gender,
        "race": profile.race,
        "nationality": profile.nationality,
        "address": profile.address,
        "city": profile.city,
        "province": profile.province,
        "country": profile.country,
        "marital_status": profile.marital_status,
    }


    for field, value in personal_fields.items():
        if not value:
            personal_missing.append(field)


    if personal_missing:

        missing_sections["personal"] = {
            "message": "Please complete all required personal details before applying for this position.",
            "missing": personal_missing
        }



    # ==================================================
    # CONTACT DETAILS CHECK
    # ==================================================

    contact = ContactDetail.objects.filter(
        profile=profile
    ).first()


    contact_missing = []


    if not contact:

        contact_missing = [
            "email",
            "phone_primary"
        ]

    else:

        if not contact.email:
            contact_missing.append("email")


        if not contact.phone_primary:
            contact_missing.append("phone_primary")



    if contact_missing:

        missing_sections["contact"] = {
            "message": "Email and primary phone number are required before applying.",
            "missing": contact_missing
        }



    # ==================================================
    # DOCUMENTS CHECK
    # ==================================================

    attachment = Attachment.objects.filter(
        profile=profile
    ).first()


    document_missing = []


    if not attachment:

        document_missing = [
            "resume",
            "id_document"
        ]

    else:

        if not attachment.resume:
            document_missing.append("resume")


        if not attachment.id_document:
            document_missing.append("id_document")



    if document_missing:

        missing_sections["documents"] = {
            "message": "Resume and ID document are required before applying.",
            "missing": document_missing
        }



    # ==================================================
    # REDIRECT IF PROFILE IS INCOMPLETE
    # ==================================================

    if missing_sections:

        # Default alert values
        alert_section = None
        alert_message = ""
        alert_missing = []


        # Priority order:
        # Personal -> Contact -> Documents

        if "personal" in missing_sections:

            alert_section = "personal"

            alert_message = (
                missing_sections["personal"]["message"]
            )

            alert_missing = (
                missing_sections["personal"]["missing"]
            )


        elif "contact" in missing_sections:

            alert_section = "contact"

            alert_message = (
                missing_sections["contact"]["message"]
            )

            alert_missing = (
                missing_sections["contact"]["missing"]
            )


        elif "documents" in missing_sections:

            alert_section = "documents"

            alert_message = (
                missing_sections["documents"]["message"]
            )

            alert_missing = (
                missing_sections["documents"]["missing"]
            )


        request.session["profile_alert"] = {

            "section": alert_section,

            "message": alert_message,

            "missing": alert_missing,

            "sections": missing_sections
        }


        messages.warning(
            request,
            "Please complete your profile details before applying."
        )


        return redirect("profile")


    # ==================================================
    # EXISTING APPLICATION CHECK
    # ==================================================

    if JobApplication.objects.filter(
        user=user,
        job=job
    ).exists():

        messages.info(
            request,
            "You already applied for this position."
        )

        return redirect("jobinfo", job.id)



    # ==================================================
    # CREATE APPLICATION
    # ==================================================

    JobApplication.objects.create(
        user=user,
        job=job
    )


    messages.success(
        request,
        "You have successfully applied for this position. Check your Profile to track your application and keep your profile up to date."
    )


    return redirect("jobinfo", job.id)

# =====================================================
# 21. PUBLIC FRONTEND PAGES
# =====================================================

# ---------- HOME PAGE ----------
def home(request):
    homehero, _ = HomeHero.objects.get_or_create(id=1)
    homeabout, _ = HomeAbout.objects.get_or_create(id=1)
    homeservices, _ = HomeServices.objects.get_or_create(id=1)
    homewhy, _ = HomeWhy.objects.get_or_create(id=1)

    footer, _ = Footer.objects.get_or_create(id=1)

    service_items = HomeServiceItem.objects.all().order_by("order", "id")
    why_items = HomeWhyItem.objects.all().order_by("order", "id")

    footer_services = FooterServiceItem.objects.all()
    footer_contacts = FooterContactItem.objects.all()

    return render(request, "myApp/home.html", {
        "homehero": homehero,
        "homeabout": homeabout,
        "homeservices": homeservices,
        "service_items": service_items,
        "homewhy": homewhy,
        "why_items": why_items,
        "footer": footer,
        "footer_services": footer_services,
        "footer_contacts": footer_contacts,
    })


# ---------- ABOUT PAGE ----------
def about(request):
    about, created = AdminAbout.objects.get_or_create(id=1)
    hero = AboutHero.objects.filter(id=1).first()

    timeline = TimelineEvent.objects.all().order_by('year')
    team = TeamMember.objects.all()
    core_values = CoreValue.objects.all().order_by('order')

    return render(request, "myApp/about.html", {
        "about": about,
        "hero": hero,
        "timeline": timeline,
        "team": team,
        "core_values": core_values
    })


# ---------- SERVICES PAGE ----------
@never_cache
def services(request):
    categories = ServiceCategory.objects.prefetch_related('items').all()
    hero = ServicesHero.objects.filter(id=1).first()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.warning(request, "Please sign in to submit a request.")
            return redirect('/signin/?next=/services/')

        QuoteRequest.objects.create(
            user=request.user,
            fullname=request.POST.get("fullname"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            service=request.POST.get("service"),
            needs=request.POST.get("needs")
        )

        messages.success(request, "Your quote request has been sent successfully!")
        return redirect('services')

    return render(request, "myApp/services.html", {
        "categories": categories,
        "hero": hero
    })


# ---------- CAREERS PAGE ----------
def careers(request):
    careers_main, created = CareersMainTopics.objects.get_or_create(id=1)

    # ✅ FORCE Django to pull ALL related contents per job
    jobs = JobPost.objects.prefetch_related(
        Prefetch(
            'contents',
            queryset=JobPostContent.objects.all().order_by('id')
        )
    ).order_by("-id")

    return render(request, "myApp/careers.html", {
        "jobs": jobs,
        "careers_main": careers_main
    })


# ---------- JOB INFO PAGE ----------
def jobinfo(request, id):

    # preload ALL related contents for THIS job
    job = get_object_or_404(
        JobPost.objects.prefetch_related(
            Prefetch(
                "contents",
                queryset=JobPostContent.objects.all().order_by("id")
            )
        ),
        id=id
    )

    already_applied = False

    if request.user.is_authenticated:

        already_applied = JobApplication.objects.filter(
            user=request.user,
            job=job
        ).exists()

    return render(
        request,
        "myApp/jobinfo.html",
        {
            "job": job,
            "already_applied": already_applied,
        }
    )


# ---------- CONTACT PAGE ----------
def contact(request):
    hero = ContactHero.objects.first()
    contact_boxes = MainTopicBox.objects.prefetch_related(
        "descriptions"
    ).all()

    return render(request, "myApp/contact.html", {
        "hero": hero,
        "contact_boxes": contact_boxes
    })






















@login_required
@xframe_options_exempt
def hrapplication_view(request, application_id):

    application = get_object_or_404(
        JobApplication,
        id=application_id
    )

    applicant = application.user
    job = application.job

    profile = get_object_or_404(
        Profile,
        user=applicant
    )

    try:

        contact = ContactDetail.objects.get(
            profile=profile
        )

    except ContactDetail.DoesNotExist:

        contact = None

    work_experience = WorkExperience.objects.filter(
        profile=profile
    ).order_by("-start_date")

    education = Education.objects.filter(
        profile=profile
    ).order_by("-start_date")

    try:

        attachments = Attachment.objects.get(
            profile=profile
        )

    except Attachment.DoesNotExist:

        attachments = None

    qualification_documents = QualificationDocument.objects.filter(
        profile=profile
    ).order_by("-uploaded_at")

    job_contents = JobPostContent.objects.filter(
        job=job
    )

    if application.status == "accepted":

        viewer = "HR"

    elif application.status == "admin_approved":

        viewer = "APPROVED"

    else:

        viewer = request.user.usercategory

    # Check where the popup was opened from

    source = request.GET.get(
        "source"
    )

    show_decision_buttons = False

    if source == "hrapplications":

        show_decision_buttons = True

    return render(
        request,
        "myApp/hrapplication_view.html",
        {
            "application": application,
            "job": job,
            "job_contents": job_contents,
            "applicant": applicant,
            "profile": profile,
            "contact": contact,
            "work_experience": work_experience,
            "education": education,
            "attachments": attachments,
            "qualification_documents": qualification_documents,
            "viewer": viewer,
            "show_decision_buttons": show_decision_buttons,
        }
    )

    
















@login_required
def hraccepted_candidate(request):

    accepted_candidates = (
        JobApplication.objects
        .filter(status="accepted")
        .select_related("user", "job")
        .order_by("-date_applied")
    )


    approved_candidates = (
        JobApplication.objects
        .filter(status="approved")
        .select_related("user", "job")
        .order_by("-date_applied")
    )


    return render(
        request,
        "myApp/hraccepted_candidate.html",
        {
            "accepted_candidates": accepted_candidates,
            "approved_candidates": approved_candidates,
        }
    )


@login_required
def hrrejected_candidate(request):
    rejected_candidates = (
        JobApplication.objects
        .filter(status="rejected")
        .select_related("user", "job")
        .order_by("-date_applied")
    )

    return render(request, "myApp/hrrejected_candidate.html", {
        "rejected_candidates": rejected_candidates
    })

@login_required
def hrupdate_application_status(request, application_id, status):

    application = get_object_or_404(JobApplication, id=application_id)

    if request.method == "POST":
        application.status = status
        application.save()

    # redirect based on status
    if status == "accepted":
        return redirect("hraccepted_candidate")

    elif status == "rejected":
        return redirect("hrrejected_candidate")

    elif status == "listed":
        return redirect("hraccepted_candidate")

    return redirect("hrapplications")



@login_required
def hrsend_candidate_admin(request, application_id):

    application = get_object_or_404(JobApplication, id=application_id)

    if request.method == "POST":
        application.status = "listed"
        application.save()

    return redirect("hraccepted_candidate")


@login_required
def adminaccepted_candidate(request):

    listed_candidates = (
        JobApplication.objects
        .filter(status="listed")
        .select_related("user", "job")
        .order_by("-date_applied")
    )

    return render(
        request,
        "myApp/adminaccepted_candidate.html",
        {
            "listed_candidates": listed_candidates
        }
    )







@login_required
@xframe_options_exempt
def adminapplication_view(request, application_id):

    application = get_object_or_404(
        JobApplication,
        id=application_id
    )

    applicant = application.user
    job = application.job

    profile = get_object_or_404(
        Profile,
        user=applicant
    )

    try:
        contact = ContactDetail.objects.get(
            profile=profile
        )
    except ContactDetail.DoesNotExist:
        contact = None


    work_experience = WorkExperience.objects.filter(
        profile=profile
    ).order_by("-start_date")


    education = Education.objects.filter(
        profile=profile
    ).order_by("-start_date")


    try:
        attachments = Attachment.objects.get(
            profile=profile
        )
    except Attachment.DoesNotExist:
        attachments = None


    qualification_documents = QualificationDocument.objects.filter(
        profile=profile
    ).order_by("-uploaded_at")


    job_contents = JobPostContent.objects.filter(
        job=job
    )


    viewer = "ADMIN"


    return render(
        request,
        "myApp/adminapplication_view.html",
        {
            "application": application,
            "job": job,
            "job_contents": job_contents,

            "applicant": applicant,
            "profile": profile,
            "contact": contact,

            "work_experience": work_experience,
            "education": education,

            "attachments": attachments,
            "qualification_documents": qualification_documents,

            "viewer": viewer,
        }
    )





@login_required
def adminapprove_application(request, application_id):

    application = get_object_or_404(
        JobApplication,
        id=application_id
    )

    if request.method == "POST":

        application.status = "approved"
        application.save()

    return redirect("adminaccepted_candidate")




from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


@login_required
def delete_application(request, application_id):

    application = get_object_or_404(
        JobApplication,
        id=application_id,
        user=request.user
    )

    if request.method == "POST":

        if application.status != "pending":
            messages.error(
                request,
                "This application can no longer be withdrawn."
            )
            return redirect("profile")

        application.delete()

        messages.success(
            request,
            "Your application has been withdrawn successfully."
        )

    return redirect("profile")





