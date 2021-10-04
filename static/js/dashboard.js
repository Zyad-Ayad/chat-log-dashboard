function valid_index_form() {
    if (document.getElementById("selected_channel").value == "")
    {
        document.getElementById("select_error").innerHTML = "Select channel first!"
        return false;
    }
    else
    {
        return true;
    }
}