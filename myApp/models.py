from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone


# =====================================================
# 1. AUTHENTICATION & USER MANAGEMENT
# =====================================================

class CustomUser(AbstractUser):
    """Custom user model with role-based categories"""
    USER_CATEGORIES = (
        ('customer', 'Customer'),
        ('hr', 'HR'),
        ('admin', 'Admin'),
    )

    usercategory = models.CharField(
        max_length=20,
        choices=USER_CATEGORIES,
        default='customer'
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class EmailVerification(models.Model):
    """Email verification tokens for user registration"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_verification"
    )

    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(hours=24)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Verification for {self.user.username}"


class PasswordReset(models.Model):
    """Password reset tokens for forgotten passwords"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(hours=1)
        super().save(*args, **kwargs)


# =====================================================
# 2. USER PROFILE & DETAILS
# =====================================================

class Profile(models.Model):
    """User profile containing personal and address information"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # PERSONAL DETAILS
    middle_name = models.CharField(max_length=50, blank=True)
    id_number = models.CharField(max_length=20, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    race = models.CharField(max_length=50, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    marital_status = models.CharField(max_length=20, blank=True)

    # ADDRESS DETAILS
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    province = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username


class ContactDetail(models.Model):
    """User contact information (email, phone, social links)"""
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE
    )

    email = models.EmailField(blank=True)
    phone_primary = models.CharField(max_length=20, blank=True)
    phone_alternative = models.CharField(max_length=20, blank=True)
    linkedin = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)

    def __str__(self):
        return f"{self.profile.user.username} Contact"


class WorkExperience(models.Model):
    """User's work history and employment details"""
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    company = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    currently_working = models.BooleanField(default=False)
    reason_for_leaving = models.TextField(blank=True, null=True)


class Education(models.Model):
    """User's educational background"""
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    school_name = models.CharField(max_length=100, blank=True, null=True)
    qualification = models.CharField(max_length=100, blank=True, null=True)
    qualification_level = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.school_name or "Education Record"


class Attachment(models.Model):
    """Main user documents (resume, ID, matric certificate)"""
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE
    )

    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    id_document = models.FileField(upload_to="ids/", blank=True, null=True)
    matric_certificate = models.FileField(upload_to="matric/", blank=True, null=True)

    def __str__(self):
        return f"{self.profile.user.username} Attachments"


class QualificationDocument(models.Model):
    """Additional qualification documents beyond the main ones"""
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    qualification_name = models.CharField(max_length=255, blank=True, null=True)
    certificate = models.FileField(upload_to="qualifications/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.qualification_name or "Qualification"


# =====================================================
# 3. JOB & CAREER MANAGEMENT
# =====================================================

class JobPost(models.Model):
    """Job listings posted by the company"""
    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=50)
    work_hours = models.CharField(max_length=50)
    stipend = models.CharField(max_length=50)
    publish_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.job_title

    class Meta:
        verbose_name = "Admin Career Job Post"
        verbose_name_plural = "Admin Career Job Posts"


class JobPostContent(models.Model):
    """Detailed content sections for each job posting"""
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name="contents")
    topic_title = models.CharField(max_length=200)
    title_level = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    format_type = models.CharField(max_length=20)

    def __str__(self):
        return self.topic_title
    
    class Meta:
        verbose_name = "Admin Career Job Post Content"
        verbose_name_plural = "Admin Career Job Post Contents"


    
class JobApplication(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('listed', 'Listed'),
        ('approved', 'Approved by Admin'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    date_applied = models.DateTimeField(auto_now_add=True)


# =====================================================
# 4. HERO IMAGES (All Pages)
# =====================================================

class HeroPhoto(models.Model):
    """Hero banner images for different pages"""
    PAGE_CHOICES = (
        ("home", "Home"),
        ("about", "About"),
        ("services", "Services"),
        ("careers", "Careers"),
        ("contact", "Contact"),
    )

    page = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
    image = models.ImageField(upload_to="hero_photos/")

    def __str__(self):
        return self.page
    
    class Meta:
        verbose_name = "Admin Hero Photo"
        verbose_name_plural = "Admin Hero Photos"


# =====================================================
# 5. HOME PAGE CONTENT
# =====================================================

class HomeHero(models.Model):
    """Home page hero section"""
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    coverage = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "Home Hero"

    class Meta:
        verbose_name = "Admin Home Hero"
        verbose_name_plural = "Admin Home Heros"


class HomeAbout(models.Model):
    """Home page about section"""
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    paragraph1 = models.TextField(blank=True, null=True)
    paragraph2 = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='home_about/', blank=True, null=True)
    years = models.CharField(max_length=10, blank=True, null=True)
    vehicles = models.CharField(max_length=10, blank=True, null=True)
    deliveries = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return "Home About"

    class Meta:
        verbose_name = "Admin Home About"
        verbose_name_plural = "Admin Home Abouts"


class HomeServices(models.Model):
    """Home page services section (deprecated/legacy)"""
    section_title = models.CharField(max_length=255, blank=True, null=True)
    section_subtitle = models.CharField(max_length=255, blank=True, null=True)
    services_data = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Home Services"
    
    class Meta:
        verbose_name = "Admin Home Service"
        verbose_name_plural = "Admin Home Services"


class HomeServiceItem(models.Model):
    """Individual service items displayed on home page"""
    icon = models.CharField(max_length=100, default="fas fa-box")
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Admin Home Service Item"
        verbose_name_plural = "Admin Home Service Items"


class HomeWhy(models.Model):
    """Home page "Why Choose Us" section"""
    section_title = models.CharField(max_length=255, blank=True, null=True)
    section_subtitle = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "Home Why"

    class Meta:
        verbose_name = "Admin Home Why"
        verbose_name_plural = "Admin Home Whys"


class HomeWhyItem(models.Model):
    """Individual "Why Choose Us" items"""
    icon = models.CharField(max_length=100, default="fas fa-truck")
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Admin Home Why Item"
        verbose_name_plural = "Admin Home Why Items"


# =====================================================
# 6. ABOUT PAGE CONTENT
# =====================================================

class AboutHero(models.Model):
    """About page hero section"""
    tagline = models.CharField(max_length=255, blank=True, null=True)
    hero_title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "About Hero"
    
    class Meta:
        verbose_name = "Admin About Hero"
        verbose_name_plural = "Admin About Heros"


class AdminAbout(models.Model):
    """About page main content"""
    history_title = models.CharField(max_length=200, default="COMPANY HISTORY", blank=True)
    history_subtitle = models.CharField(max_length=200, default="Built on Dedication Since 2016", blank=True)
    history_p1 = models.TextField(blank=True)
    history_p2 = models.TextField(blank=True)
    history_p3 = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "About Page Content"
    
    class Meta:
        verbose_name = "Admin About"
        verbose_name_plural = "Admin Abouts"


class TimelineEvent(models.Model):
    """Company history timeline events"""
    year = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.year} - {self.description}"

    class Meta:
        ordering = ["order", "year"]
        verbose_name = "Admin About Timeline Event"
        verbose_name_plural = "Admin About Timeline Events"


class TeamMember(models.Model):
    """Team member profiles"""
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    bio = models.TextField()
    photo = models.ImageField(upload_to='team/')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.role}"

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Admin About Team Member"
        verbose_name_plural = "Admin About Team Members"


class CoreValue(models.Model):
    """Company core values"""
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Admin About Core Value"
        verbose_name_plural = "Admin About Core Values"


# =====================================================
# 7. SERVICES PAGE CONTENT
# =====================================================

class ServicesHero(models.Model):
    """Services page hero section"""
    tagline = models.CharField(max_length=255, blank=True, null=True)
    hero_title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "Services Hero"

    class Meta:
        verbose_name = "Admin Service Hero"
        verbose_name_plural = "Admin Service Heros"


class ServiceCategory(models.Model):
    """Service categories"""
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Admin Service Category"
        verbose_name_plural = "Admin Service Categories"


class ServiceItem(models.Model):
    """Individual services within a category"""
    category = models.ForeignKey(
        ServiceCategory,
        related_name="items",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=100, default="fas fa-cog")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Admin Service Item"
        verbose_name_plural = "Admin Service Items"


# =====================================================
# 8. CAREERS PAGE CONTENT
# =====================================================

class CareersMainTopics(models.Model):
    """Careers page main content sections"""
    tagline = models.CharField(max_length=200, blank=True, null=True)
    hero_title = models.CharField(max_length=255, blank=True, null=True)
    intro_title = models.CharField(max_length=255, blank=True, null=True)
    intro_text = models.TextField(blank=True, null=True)
    open_positions_title = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Careers Main Page Content"

    class Meta:
        verbose_name = "Admin Career Main Topic"
        verbose_name_plural = "Admin Career Main Topics"


# =====================================================
# 9. CONTACT PAGE CONTENT
# =====================================================

class ContactHero(models.Model):
    """Contact page hero section"""
    tagline = models.CharField(max_length=255)
    hero_title = models.CharField(max_length=255)

    def __str__(self):
        return "Contact Hero"
    
    class Meta:
        verbose_name = "Admin Contact Hero"
        verbose_name_plural = "Admin Contact Heros"


class MainTopicBox(models.Model):
    """Contact page main topic boxes"""
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Admin Contact Main Topic Box"
        verbose_name_plural = "Admin Contact Main Topic Boxs"


class TopicDescription(models.Model):
    """Descriptions within contact topic boxes"""
    box = models.ForeignKey(
        MainTopicBox,
        related_name="descriptions",
        on_delete=models.CASCADE
    )
    text = models.TextField()

    def __str__(self):
        return self.text[:30]

    class Meta:
        verbose_name = "Admin Contact Topic Description"
        verbose_name_plural = "Admin Contact Topic Descriptions"


# =====================================================
# 10. SITE WIDE (Header & Footer)
# =====================================================

class SiteHeader(models.Model):
    """Global site header configuration"""
    company_name = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='site_header/', blank=True, null=True)

    def __str__(self):
        return self.company_name or "Site Header"

    class Meta:
        verbose_name = "Admin Site Header"
        verbose_name_plural = "Admin Site Headers"


class Footer(models.Model):
    """Global site footer configuration"""
    company_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Footer"

    class Meta:
        verbose_name = "Admin Footer"
        verbose_name_plural = "Admin Footers"


class FooterServiceItem(models.Model):
    """Footer service links/items"""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Admin Footer Service Item"
        verbose_name_plural = "Admin Footer Service Items"


class FooterContactItem(models.Model):
    """Footer contact information"""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Admin Footer Contact Item"
        verbose_name_plural = "Admin Footer Contact Items"


# =====================================================
# 11. QUOTE REQUESTS
# =====================================================

class QuoteRequest(models.Model):
    """User quote/service requests"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    fullname = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=100)
    needs = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname
    
    class Meta:
        verbose_name = "User Quote Request Service"
        verbose_name_plural = "User Quote Request Services"








