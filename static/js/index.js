function valid_index_form() {
    if (document.getElementById("selected_server").value == "")
    {
        document.getElementById("select_error").innerHTML = "Select server first!"
        return false;
    }
    else
    {
        return true;
    }
}
