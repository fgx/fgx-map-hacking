from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    
    
    ## Fix
    url(r'^ajax/fix$', 'nav.views.fix', name='fix'),
    url(r'^ajax/fix/(?P<ident>\w{0,6})$', 'nav.views.fix', name='fix'),
    
    
    ## xplane
    url(r'^ajax/xplane/avail$', 'xplane.views.avail', name='xplane'),
    #url(r'^ajax/fix/(?P<ident>\w{0,6})$', 'fix.views.fix', name='fix'),
    
    
    ## Maps
     url(r'^map/(?P<map_name>\w{0,6})$', 'xmap.views.map', name='map'),
    
    ## Main
    url(r'^$', 'xmap.views.index', name='index'),
    
    
    
    #url(r'^fgxmap/', include('fgxmap.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
)
