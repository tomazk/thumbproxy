Thumbnail Proxy
===============

lazy and seamless generation of thumbnails

*dirty but fun hackday project at Zemanta*

Setup
-----

* setup instance on ec2 
* deploy app.py flask application (nginx + gunicorn)
  * copy localsettings.template 
  * generate secret with bin/generate_secret.py and copy it into localsettings.SECRET
* create new cloudfront distribution and put it in front of the newly deployed service (make sure to forward query strings to origin)

Example 
-------
```
  # copy secret into example/secret.py
  
  # sign an example url
  python example/sign_url.py "http://yourCF.cloudfront.net/api/?u=http://example.com/img.jpg&a=thumb&w=500&h=300"
  
  # returns signed url 
  > http://yourCF.cloudfront.net/api/?u=http://example.com/img.jpg&a=thumb&w=500&h=300&s={SIGNATURE}"
```

