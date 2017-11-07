from pydantic import BaseModel


class Logo(BaseModel):
    img_url: str = None
    img_file: str = None
    alt: str = None


class SocialMedia(BaseModel):
    twitter: str = None
    github: str = None


class SiteConfig(BaseModel):
    logo: Logo = None
    social_media: SocialMedia = None
    copyright = 'All Rights Reserved'
    is_debug = False
