## 接口

/myapp/login/

body包含：username、password（返回的expire是token过期时间）

/myapp/token/refresh/

body包含refresh，刷新token

/myapp/token/verify/

body包含token，检查token是否过期

/myapp/register/

body包含：username、password、confirm_password、email

会直接返回token和refresh