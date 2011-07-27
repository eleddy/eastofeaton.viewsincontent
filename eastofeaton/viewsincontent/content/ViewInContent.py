from Products.Archetypes import atapi
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content import schemata
from zope.interface import implements
from zope.app.component.hooks import getSite
from eastofeaton.viewsincontent import config
from eastofeaton.viewsincontent.interfaces import IViewInContent
from plone.app.customerize import registration
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.browser.interfaces import IBrowserView
from zope.viewlet.interfaces import IViewlet
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from eastofeaton.viewsincontent.interfaces import IContentCoreSnippit
from lxml import etree


ViewInContentSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    atapi.LinesField('view',
        searchable=1,
        required=1,
        widget=atapi.MultiSelectionWidget(
            label=u'Select a view to display',
            format='checkbox'),
        vocabulary='viewVocab',
        ),
    ))
    
ViewInContentSchema['title'].required = 0

class ViewInContent(ATCTContent):
    schema = ViewInContentSchema
    implements(IViewInContent)
    
    def viewVocab(self): 
        """
        Return a list of all athletes, used in the dropdown menu 
        """ 
        mapping = []
        views = registration.getViews(IBrowserRequest)
        for view in views:
            if view.name and self.getRenderableView(view.name):
                mapping.append((view.name, view.name))
        return atapi.DisplayList(mapping)
        
    def getRenderableView(self, viewName):
        context = aq_inner(self)
        try:
            return getMultiAdapter((context, self.REQUEST), name=viewName)
        except: 
            return None
    
    def getSnippits(self):
        """
        Get the views. For each view, render the content. Currently, 
        this looks for an id of "content" and filters on that if it 
        exists. 
        XXX: There has to be a better way to do this
        """
        snippits = []
        for viewName in self.view:
            view = self.getRenderableView(viewName)
            if view:
                view = view.__of__(self)
                snippit = view.render()
            
                root = etree.HTML(snippit)
                contentRoot = root.xpath("//*[@id='content']")
                if len(contentRoot):
                    root = contentRoot[0]
                snippits.append(etree.tostring(root, method="html"))
            
        return snippits
    

atapi.registerType(ViewInContent, config.PROJECTNAME)
