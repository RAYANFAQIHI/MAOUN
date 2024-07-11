// يمكنك إضافة تفاعلات JavaScript هنا
document.querySelectorAll('.toolbar-btn').forEach(button => {
    button.addEventListener('click', () => {
        alert(button.title + ' تم النقر عليه');
    });
});
function enableToolbarButtons() {
    document.getElementById('btn-open').disabled = false;
    document.getElementById('btn-download').disabled = false;
    // تفعيل باقي الأزرار حسب الحاجة
}

function disableToolbarButtons() {
    document.getElementById('btn-open').disabled = true;
    document.getElementById('btn-download').disabled = true;
    // تعطيل باقي الأزرار حسب الحاجة
}
function handleFileUpload() {
    // إجراءات رفع الملف
    // عند الانتهاء من رفع الملف، فعّل الأزرار في شريط الأدوات
    enableToolbarButtons();
}
