# Rewrite

- Before

    * Commit history to changelog investigation
    
    * Semver and extract investigation
    
    * pbr investigation
    
    * Fixtures for Sphinx env.*
    
- New repo, kill version history

- Switch to pbr and humane packaging

- Good commit history changelog plan

- Travis or whoever

- Test coverage regime as part of CI

- Blank docs, write docs before adding back in each thing

- Commit to pipenv

- Update all dependencies

- Replace debug with a builder like sphinxcontrib-needs

- Use logging

# Re-org

- kaybee_resources, kaybee_widgets, kaybee_articles, kaybee_postrender,
  kaybee_feeds, kaybee_site

- Move all the methods off of Site

- resource loses a lot of the schema

- Make simple example based on built-in resource directive

- Get rid of genericpage, everything is a resource

# Now

- A model with a ReferenceField doesn't fail when the value points at 
  a non-existent reference

- The TemplateBridge postrender should not apply to widgets

# Next

- RST-rendered field type and excerpt

- Get rid of make_context on widgets

- Have a date format in config like ablog line 280 post.py

- Like ablog, get title in resources.events using node['title'] or 
  _get_section_title
  
- Multiple feeds  

- Make relative/absolute URLs work, e.g. /blog vs. Sphinx rendered with 
  "pathto" available in widgets
  
- Break resources, widgets, etc. into plugin packages

- Have a basic "resource" that can be used in docs

- Feed publish dates with configurable timezones

- Redirects like ABlog

- Get LiveSearch box working

- Icon for LiveSearch box

- Pluggable SiteConfig

- Pluggable toctree

- Pluggable "layout"

- Release a package

- Document the development setup

    - Running app.py
    
    - npm start

# Later

- Restructure everything to make it easy to jump from code -> test

# Done 

- Change from feedgen to something not requiring lxml

