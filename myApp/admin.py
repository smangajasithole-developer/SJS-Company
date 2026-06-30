from django.contrib import admin
from .models import (
    
    # USER
    CustomUser,
    QuoteRequest,
    Profile,
    ContactDetail,
    WorkExperience,
    Education,
    Attachment,
    QualificationDocument,
    JobApplication,

    # ABOUT
    AboutHero,
    AdminAbout,
    TimelineEvent,
    TeamMember,
    CoreValue,
    HeroPhoto,

    # SERVICES (MAIN SITE)
    ServiceCategory,
    ServiceItem,
    ServicesHero,

    # JOBS
    JobPost,
    JobPostContent,

    # CAREERS
    CareersMainTopics,

    # CONTACT
    ContactHero,
    MainTopicBox,
    TopicDescription,

    # HOME PAGE
    HomeHero,
    HomeAbout,
    HomeServices,
    HomeServiceItem,
    HomeWhy,
    HomeWhyItem,

    # HEADER / FOOTER
    SiteHeader,
    Footer,
    FooterServiceItem,
    FooterContactItem,
)

# =========================================================
# USERS
# =========================================================
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "usercategory")
    list_filter = ("usercategory",)
    search_fields = ("username", "email")


# =========================================================
# QUOTES
# =========================================================
@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "service", "created_at")
    search_fields = ("fullname", "email", "service")
    list_filter = ("created_at",)







# -------------------------
# PROFILE CORE
# -------------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "id_number",
        "gender",
        "nationality",
        "city",
        "province"
    )
    search_fields = ("user__username", "user__email", "id_number")
    list_filter = ("gender", "nationality", "province")


# -------------------------
# CONTACT DETAILS
# -------------------------
@admin.register(ContactDetail)
class ContactDetailAdmin(admin.ModelAdmin):
    list_display = ("profile", "phone_primary", "phone_alternative")
    search_fields = ("profile__user__username", "phone_primary")


# -------------------------
# WORK EXPERIENCE
# -------------------------
@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "profile",
        "company",
        "job_title",
        "start_date",
        "end_date",
        "currently_working"
    )
    list_filter = ("currently_working", "company")
    search_fields = ("company", "job_title", "profile__user__username")


# -------------------------
# EDUCATION
# -------------------------
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = (
        "profile",
        "school_name",
        "qualification",
        "qualification_level",
        "start_date",
        "end_date"
    )
    search_fields = ("school_name", "qualification", "profile__user__username")


# -------------------------
# ATTACHMENTS
# -------------------------
@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = (
        "profile",
        "resume",
        "id_document",
        "matric_certificate"
    )
    search_fields = ("profile__user__username",)






# =========================================================
# ABOUT PAGE
# =========================================================
@admin.register(AboutHero)
class AboutHeroAdmin(admin.ModelAdmin):
    list_display = ("tagline", "hero_title")


@admin.register(AdminAbout)
class AdminAboutAdmin(admin.ModelAdmin):
    list_display = ("history_title", "updated_at")


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ("year", "description", "order")
    ordering = ("order",)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order")
    ordering = ("order",)


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    ordering = ("order",)


# =========================================================
# SERVICES (MAIN SITE PAGE)
# =========================================================
class ServiceItemInline(admin.TabularInline):
    model = ServiceItem
    extra = 1


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    inlines = [ServiceItemInline]


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "icon", "created_at")
    list_filter = ("category",)


@admin.register(ServicesHero)
class ServicesHeroAdmin(admin.ModelAdmin):
    list_display = ("tagline", "hero_title")


# =========================================================
# JOBS
# =========================================================
@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ("job_title", "company_name", "location", "closing_date")


@admin.register(JobPostContent)
class JobPostContentAdmin(admin.ModelAdmin):
    list_display = ("job", "topic_title", "title_level")


# =========================================================
# CAREERS
# =========================================================
@admin.register(CareersMainTopics)
class CareersMainTopicsAdmin(admin.ModelAdmin):
    list_display = ("hero_title", "updated_at")


# =========================================================
# CONTACT
# =========================================================
class TopicDescriptionInline(admin.TabularInline):
    model = TopicDescription
    extra = 1


@admin.register(MainTopicBox)
class MainTopicBoxAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [TopicDescriptionInline]


@admin.register(TopicDescription)
class TopicDescriptionAdmin(admin.ModelAdmin):
    list_display = ("box", "text")


# =========================================================
# HOME PAGE
# =========================================================
@admin.register(HomeHero)
class HomeHeroAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "coverage")
    search_fields = ("title", "subtitle")


@admin.register(HomeAbout)
class HomeAboutAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "years", "vehicles", "deliveries")


@admin.register(HomeServices)
class HomeServicesAdmin(admin.ModelAdmin):
    list_display = ("section_title", "section_subtitle")


@admin.register(HomeServiceItem)
class HomeServiceItemAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order")
    list_editable = ("order",)
    search_fields = ("title",)
    ordering = ("order",)


@admin.register(HomeWhy)
class HomeWhyAdmin(admin.ModelAdmin):
    list_display = ("section_title", "section_subtitle")


@admin.register(HomeWhyItem)
class HomeWhyItemAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order")
    list_editable = ("order",)
    search_fields = ("title",)
    ordering = ("order",)


# =========================================================
# SITE HEADER
# =========================================================
@admin.register(SiteHeader)
class SiteHeaderAdmin(admin.ModelAdmin):
    list_display = ("company_name",)


# =========================================================
# FOOTER
# =========================================================
@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ("company_name",)


@admin.register(FooterServiceItem)
class FooterServiceItemAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(FooterContactItem)
class FooterContactItemAdmin(admin.ModelAdmin):
    list_display = ("title", "link")



#====================================================================

@admin.register(HeroPhoto)
class HeroPhotoAdmin(admin.ModelAdmin):
    list_display = ("page",)


# -------------------------
# QUALIFICATION DOCUMENTS
# -------------------------
@admin.register(QualificationDocument)
class QualificationDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "profile",
        "qualification_name",
        "certificate",
        "uploaded_at"
    )

    search_fields = (
        "profile__user__username",
        "qualification_name",
    )

    list_filter = (
        "uploaded_at",
    )

# -------------------------
# JOB APPLICATIONS (IMPORTANT FOR NEXT STEP)
# -------------------------
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "job",
        "status",
        "date_applied",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "user__email",
        "job__job_title",
    )