function Remove() {
    var choosed_user = document.getElementById("user_to_add").options[document.getElementById("user_to_add").selectedIndex].text;
    var choosed_list = document.getElementById("list_to_add").options[document.getElementById("list_to_add").selectedIndex].text;
    // alert(choosed_user+choosed_list);
    window.location = Flask.url_for("manager", {"choosed_user": choosed_user, "choosed_list": choosed_list});
    return false;
}

//
// $(document).ready(function() {
//     $('[id^="a#list_"]').on('click', function (event) {
//         event.preventDefault();
//         $.ajax({
//             data : { list_id: $(this).attr('id') },
//             type : 'GET',
//             url : '/get_todo_items',
//             success : function (data) {
//                 if (data) {
//                     $('div#list_content').innerHTML=data
//                 }
//             },
//             error : function () {
//                 $('div#list_content').innerHTML="Failed to load data"
//             }
//
//         });
//
//     });
// });
// $("button").click(function(){
//         $("p").hide(1000);
//     });

// $("button").click(function(){
//     $("p").toggle();
// });

// $(document).ready(function(){
//     $("button").click(function(){
//         $("#div1").fadeOut();
//         $("#div2").fadeOut("slow");
//         $("#div3").fadeOut(3000);
//     });
// });

//
// $("button").click(function(){
//     $("#div1").fadeToggle();
//     $("#div2").fadeToggle("slow");
//     $("#div3").fadeToggle(3000);
// });

// $(document).ready(function() {
//     $('[id^="list_"]').on('click', function (event) {
//         var list_id = $(this).attr('id');
//         // $('div#list_content').html(info);
//
//             $.ajax ({
//                 data : {choosed_list_id : list_id},
//                 type : 'POST',
//                 url : 'list_todo_items',
//                 // contentType: 'html',
//                 dataType: 'html',
//                 success : function (status) {
//                     $('div#list_content').html(status.text)
//                 }
//             });
//
//         event.preventDefault();
//     });
//
//
//     //     $.post("demo_test_post.asp",
//     //     {
//     //       name: "Donald Duck",
//     //       city: "Duckburg"
//     //     },
//     //     function(data,status){
//     //         alert("Data: " + data + "\nStatus: " + status);
//     //     });
//     // });
// });