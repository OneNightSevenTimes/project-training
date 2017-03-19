from django import forms



forms基础:

1.定义一个forms表单类:
class HostGroupForm(forms.Form):
    email = forms.EmailField(required=False,
                             error_messages={'required':u'邮箱地址不能为空','invalid':u'邮箱地址格式错误'}

    )
    host = forms.CharField()
    port = forms.IntegerField()
    password = forms.PasswordInput()


2.定义views方法:
    1.返回表单页面
    2.验证提交的数据是否合法

def index(request):
    obj = HostGroupForm()  ##生成form表单对象
    if request.method == 'POST':
        user_input_obj = HostGroupForm(request.POST)  ##封装提交来的数据
        is_valid= user_input_obj.is_valid() ##验证数据是否合法
        if is_valid:
            data = user_input_obj.cleaned_data() ##获取提交的数据
        else:
            errors_msg = user_input_obj.errors  ##捕捉不合法的错误

        return render(request,'index.html',{'obj':user_input_obj,'errors':errors_msg})
    return render(request,'index.html',{'obj':obj})


index.html

    <div>
        <from method='GET',action=''>
           <p>主机: {{ obj.host}} <span>{{ errors.host}}</span></p>
           <p>端口: {{ obj.port }}<span>{{ errors.port}}</span></p>
           <input type='submit'/>
        </form>
    </div>

required:是否可以为空 false,可以为空,true不能为空



#################




import re
from django.core.exceptions import ValidationError
def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[0-9]|17[678]|18[0-9]|14[5-7])[0-9]{8}]')
    if not mobile_re.match(value):
        raise ValueError('手机号码格式错误')


class HostGroupForm(forms.Form):
    user_type_choice = (
        (0,u'超级用户'),
        (1.u'普通用户'),
    )
    user_type = forms.IntegerField(widget=forms.Select(choices=user_type_choice,attrs={'class':'form-control'}))
    email = forms.EmailField(required=False,
                             error_messages={'required':u'邮箱地址不能为空','invalid':u'邮箱地址格式错误'}

    )
    host = forms.CharField(error_messages={'required':u'主机不能为空','invalid':u'主机格式错误'})
    port = forms.IntegerField(error_messages={'required':u'端口不能为空','invalid':u'端口格式错误'})
    password = forms.PasswordInput(error_messages={'required':u'密码不能为空','invalid':u'密码格式错误'},
                                   widget=forms.TextInput(attrs={'class':'form-control',
                                                                 'placeholder':'请输入密码'}))
    mobile = forms.CharField(validators=[mobile_validate,],
                             error_messages={'required':u'手机地址不能为空','invalid':u'手机格式错误'},
                             widget=forms.TextInput(attrs={'class':'form-control',
                                                           'placeholder':u'请输入手机号码'}))



required: 是否可以为空.默认为True,不能为空
errors_messages:验证数据优雅显示 , error_messages={'required':u'手机地址不能为空','invalid':u'手机格式错误'}

validators:列表里面自定义验证方法 mobile_validate()方法
widget:插件对应html里面的标签