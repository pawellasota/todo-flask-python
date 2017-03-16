$(document).ready(function() {
    $('#all_lists').on('click', '[id^=list_]', function (event) {
        event.preventDefault();
        var list_id = this.id;
        $('div#l_content').slideUp("slow", function () {
            $.ajax({
                data : { list_id: list_id },
                type : 'GET',
                url : '/get_todo_items',
                success : function (data) {
                    if (data) {
                        $('div#e_content').slideUp("slow");
                        $('div#a_content').slideUp("slow");
                        $('div#a_l_content').slideUp("slow");
                        $('div#l_content').slideDown("slow");
                        $('div#l_content').html(data)
                    }
                },
                error : function () {
                    $('div#l_content').innerHTML="Failed to load data"
                }

            });
        });
    });
    $(document).on('change', '[class^=todo_]', function (event) {
        var todo_id = $(this).attr('class');
        $.ajax({
            data : { todo_id: todo_id},
            type : 'GET',
            url : '/toggle',
            success: function (data) {
                if (data == "True") {
                    $('#info').text("Todo item saved as marked").show();
                }
                else {
                    $('#info').text("Todo item saved as unmarked").show();
                }
                $('#info').delay(2000).fadeOut('slow');
            },
            error : function () {
                alert("Toggle error")
            }
        });
    });
    $(document).on('click', '[id^=remove_]', function (event) {
        event.preventDefault();
        var todo_id = $(this).attr('id');
        $.ajax({
            data : { todo_id : todo_id},
            type : 'GET',
            context: this,
            url : '/remove',
            success : function (data) {
                $('#info').text("Todo removed: " + data.todo_name).show();
                $('#info').delay(2000).fadeOut('slow');
                $(this).closest('tr').fadeOut("slow");
            },
            error : function () {
                alert("Remove error")
            }
        })
    });
    $(document).on('click', '[id^=edit_]', function (event) {
        event.preventDefault();
        var todo_id = $(this).attr('id');
        $('div#l_content').slideUp("slow");
        $('div#e_content').slideDown("slow", function () {
            $.ajax({
                data : { todo_id : todo_id},
                type : 'GET',
                url : '/edit',
                success : function (data) {
                    $('div#e_content').slideDown("slow");
                    $('div#e_content').html(data);
                },
                error : function () {
                    alert("Cannot add todo item!")
                }
            })
        })
    });
    $(document).on('click', '[id^=update_todo_]', function (event) {
        event.preventDefault();
        var todo_id = $(this).attr('id');
        var todo_name = $('#todo_name').val();
        var todo_due_date = $('#todo_due_date').val();
        var todo_priority = $('#todo_priority').val();
        var update_todo_list_id = $('#update_todo_list_id').val();
        $.ajax({
            data : { todo_id : todo_id,
                     todo_name : todo_name,
                     todo_due_date : todo_due_date,
                     todo_priority : todo_priority },
            type : 'POST',
            url : '/edit',
            success : function (data) {
                jQuery("#list_"+update_todo_list_id)[0].click();
                $('#info').text("Todo updated: "+ data.todo_name).show();
                $('#info').delay(2000).fadeOut('slow');
            },
            error: function (data) {
                alert(data)
            }
        })
    });
    $(document).on('click', '[id^=add_new_todo_]', function (event) {
        event.preventDefault();
        var choosed_list_id = $(this).attr('id');
        $.ajax({
            data : { choosed_list_id : choosed_list_id },
            type : 'GET',
            url : '/add',
            success : function (data) {
                $('div#l_content').slideUp("slow");
                $('div#e_content').slideUp("slow");
                $('div#a_content').html(data);
                $('div#a_content').slideDown('slow');
            },
            error : function (data) {
                alert('Add item aborted')
            }
        })
    });
    $(document).on('click', '[id^=add_todo_submit_]', function (event) {
        event.preventDefault();
        var choosed_list_id = $(this).attr('id');
        var todo_name = $('#todo_name_submit').val();
        var todo_due_date = $('#todo_due_date_submit').val();
        var todo_priority = $('#todo_priority_submit').val();
        $.ajax({
            data : { choosed_list_id : choosed_list_id,
                     todo_name : todo_name,
                     todo_due_date : todo_due_date,
                     todo_priority : todo_priority },
            type : 'POST',
            url : '/add',
            context : this,
            success : function (data) {
                var trigger_button = choosed_list_id.replace('add_todo_submit_','');
                jQuery("#list_"+trigger_button)[0].click();
                $('#info').text("Todo added: "+ data.item_content).show();
                $('#info').delay(2000).fadeOut('slow');
            },
            error : function (data) {
                alert("Error in adding todo")
            }
        })
    });
    $(document).on('click', '[id=add_new_list]', function (event) {
        event.preventDefault();
        $.ajax({
            type : 'GET',
            url : '/addlist',
            success: function (data) {
                $('div#l_content').slideUp("slow");
                $('div#e_content').slideUp("slow");
                $('div#a_content').slideUp('slow');
                $('#a_l_content').slideDown('slow');
                $('#a_l_content').html(data);
            },
            error: function () {
                alert("Cannot add list")
            }
        })
    });
    $(document).on('click', '#add_list_submit', function (event) {
        event.preventDefault();
        var list_name = $('.inpbutt').val();
        $.ajax({
            data : {list_name : list_name },
            type : 'POST',
            url : '/addlist',
            success : function (data) {
                if (data.error){
                    $('#info').text(data.error).show();
                    $('#info').delay(2000).fadeOut('slow');
                }
                else {
                    $('#info').text("List was added: "+ data.todo_list_name).show();
                    $('#info').delay(2000).fadeOut('slow');
                    $('#all_lists').append('<a class="btn btn-default btn-large" id="list_'+data.todo_list_id+'" ' +
                      'href="" role="button">'+ data.todo_list_name+'</a>');
                    $('#a_l_content').slideUp('slow');
                    jQuery("#button-list")[0].click();
                }
            },
            error : function () {
                alert("Error during creating list")
            }

        })
    });
    $(document).on('click', '[id^=rem_list_]', function (event) {
        event.preventDefault();
        var list_id = $(this).attr('id');
        $.ajax({
            data: {list_id: list_id},
            type: 'GET',
            url: '/remove_list',
            success: function (data) {
                if (data.error) {
                    $('#info').text("Error: "+ data.error).show();
                    $('#info').delay(2000).fadeOut('slow');
                }
                else {
                    $('#info').text("List: "+ data.list_name+" has been deleted").show();
                    $('#info').delay(2000).fadeOut('slow');
                    var list_button = $('#list_'+data.list_id);
                    list_button.fadeOut('slow', function () {
                        list_button.remove();
                        $('#l_content').slideUp('slow');
                    })
                }
            },
            error: function (data) {
                alert("Removing list failed")
            }
        })
    });
    $(document).on('click', '.bg-picker', function () {
        var bgcol = $(this).css('background-color');
        $('body').css("background-color", bgcol);
    });
    $(document).on('click', '.ft-picker', function () {
        var font = $(this).css('font-family');
        $('body').css("font-family", font);
    });
    $(document).on('click', '.ft-col-picker', function () {
        var bgcol = $(this).css('background-color');
        $('body').css("color", bgcol);
    })

});

function Remove() {
    var choosed_user = document.getElementById("user_to_add").options[document.getElementById("user_to_add").selectedIndex].text;
    var choosed_list = document.getElementById("list_to_add").options[document.getElementById("list_to_add").selectedIndex].text;
    // alert(choosed_user+choosed_list);
    window.location = Flask.url_for("manager", {"choosed_user": choosed_user, "choosed_list": choosed_list});
    return false;
}
