from drf_yasg import openapi


login_user_schema = openapi.Schema(
    title =("Login"),
    type=openapi.TYPE_OBJECT, 
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING,example="User@example.com"),
        'password': openapi.Schema(type=openapi.TYPE_STRING,example="password123"),
    },
    required=['email','password',],
)

register_user_schema = openapi.Schema(
    title =("Login"),
    type=openapi.TYPE_OBJECT, 
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING,example="User1@example.com"),
        'password': openapi.Schema(type=openapi.TYPE_STRING,example="password123"),
        'first_name': openapi.Schema(type=openapi.TYPE_STRING,example="Akshay"),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING,example="Sharma"),
        'mobile_no': openapi.Schema(type=openapi.TYPE_STRING,example="8791109041"),
        'description': openapi.Schema(type=openapi.TYPE_STRING,example="password123"),
        'address_line_1': openapi.Schema(type=openapi.TYPE_STRING,example="aaa"),
        'address_line_2': openapi.Schema(type=openapi.TYPE_STRING,example="bbb"),
        'city': openapi.Schema(type=openapi.TYPE_STRING,example="gurgaon"),
        'state': openapi.Schema(type=openapi.TYPE_STRING,example="haryana"),
        'country': openapi.Schema(type=openapi.TYPE_STRING,example="india"),
        'pincode': openapi.Schema(type=openapi.TYPE_STRING,example="112233"),
    },
    required=['email','password','first_name', 'last_name', 'mobile_no','description'
              'address_line_1','address_line_2','city','state','country', 'pincode'],
)