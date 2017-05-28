# Now

- Switch to reg-based and possibly merge theme and kaybee

- Have an inline directive that does querying

- Make relative/absolute URLs work, e.g. /blog vs. Sphinx rendered

- Make enough docs to represent a hierarchy

- Breadcrumbs

- Contents sidebar

- Get LiveSearch box working

- Icon for LiveSearch box

# Next

- Release a package

- Document the development setup

    - Running app.py
    
    - npm start

# Later


# Reg Thoughts

- Site

    - An adapter from the Sphinx pile of stuff, to kaybee.Site
    
    - Theme can skip Sphinx and implement something simpler

- Title

    - Function which is passed the site and the resource    
        
- Nav menu

    - A subclass of TemplateAdapter
    
    - Uses startup "sections" state from config file
    
    - Every resource has to say what section it is in with
      default to None

    - The subclass fills in the template to use, as a property
    
    - The __call__ renders to HTML
    
    - The template_context returns objects passed into the template
    
    - Increase performance by allowing it to be re-used, passing 
      per-page data into __call__
      
    - Property on the site returns the adapter
    
      
    