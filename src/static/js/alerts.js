const notificacionSwalf = (titleText,text,icon,confirmationButtonText) => {
    Swal.fire({
        titleText:titleText,
        text:text,
        icon:icon,
        confirmationButtonText:confirmationButtonText
    });
}