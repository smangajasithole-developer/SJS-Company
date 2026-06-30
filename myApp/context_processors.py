from .models import HeroPhoto, SiteHeader, Footer, FooterServiceItem, FooterContactItem


def global_context(request):
    # ================= HERO IMAGES =================
    photos = HeroPhoto.objects.all()
    hero_map = {photo.page: photo for photo in photos}

    # ================= HEADER =================
    header = SiteHeader.objects.first()

    # ================= FOOTER =================
    footer = Footer.objects.first()
    service_items = FooterServiceItem.objects.all().order_by("id")
    contact_items = FooterContactItem.objects.all().order_by("id")

    return {
        # HERO
        "hero_photos": hero_map,

        # HEADER
        "header": header,

        # FOOTER
        "footer": footer,
        "footer_services": service_items,
        "footer_contacts": contact_items,
    }