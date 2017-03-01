function Remove() {
    var choosed_user = document.getElementById("user_to_add").options[document.getElementById("user_to_add").selectedIndex].text;
    var choosed_list = document.getElementById("list_to_add").options[document.getElementById("list_to_add").selectedIndex].text;
    // alert(choosed_user+choosed_list);
    window.location = Flask.url_for("manager", {"choosed_user": choosed_user, "choosed_list": choosed_list});
    return false;
}
