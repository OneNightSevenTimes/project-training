/**
 * Created by DaoKe on 16/5/23.
 */

function CheckAll(mode,tb){
    $('#tb1').children().each(function () {
        var tr = $(this);
        var isChecked = tr.find(":checkbox").prop('checked');
        if (isChecked){
            //已经选中,取消选中
            tr.find(':checkbox').prop('checked',false);
            //如果已经进入编辑模式,让选中的行恢复编辑状态前
            var isEditing = $(mode).hasClass('editing');
            if (isEditing){
                tr.children().each(function(){
                    var td = $(this);
                    //找到可编辑的行,恢复成text内容
                    if(td.attr('edit') == 'true'){
                        var inp = td.children().first()//找到当前标签下面第一个标签就是input标签
                        var inp_val = inp.val()//获取input的value值
                        td.text(inp_val)
                    }
                })
            }
        }else{
            tr.find(':checkbox').prop('checked',true);
            //如果已经进入编辑模式,让选中的行进入编辑状态
            var isEditing = $(mode).hasClass('editing');
            if(isEditing){
                tr.children().each(function(){
                    var td = $(this);
                    //判断哪个行是可以编辑的
                    if (td.attr('edit') == 'true'){
                        var text = td.text() //获取text内容,将其替换成input标签,可编辑
                        var temp = "<input type='text' value='"+ text +"'>"
                        td.html(temp)
                    }
                })
            }
        }
    })
}

function CheckReverse(mode,tb){

}

function CheckCancel(mode,tb){

}

function EditMode(ths){
    var isEditing = $(ths).hasClass('editing');
    if (isEditing){
        $(ths).removeClass('editing');
        $(ths).text('进入编辑模式');
    }else{
        $(ths).addClass('editing');
        $(ths).text('退出编辑模式')
    }

}


function MoveToRight(from,to){
    $(from + " option").each(function(){
        var op = $(this);
        if (op.prop('selected') == true){
            $(to).append(op)
        }
    })
}

function MoveToLeft(from,to){
    $(from + " option").each(function(){
        var op = $(this);
        if (op.prop('selected') == true){
            $(to).append(op)
        }
    })
}

