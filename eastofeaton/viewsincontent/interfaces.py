from zope.interface import Interface


class IViewInContent(Interface):
    """Marker for the view in content type"""
    
class IContentCoreSnippit(Interface):
    """Mark with this interface to list as a content item"""