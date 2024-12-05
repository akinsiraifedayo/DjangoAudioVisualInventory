'use strict';

document.addEventListener('DOMContentLoaded', function (e) {
  (function () {
    const deleteButtons = document.querySelectorAll('.delete-transaction');
    deleteButtons.forEach(deleteButton => {
      deleteButton.addEventListener('click', function (e) {
        e.preventDefault();
        const product = this.getAttribute('data-transaction-product');
        const warehouse = this.getAttribute('data-transaction-warehouse');
        const items = this.getAttribute('data-transaction-items');
        Swal.fire({
          title: 'Delete Warehouse Stock?',
          html: `<p class="text-danger">Are you sure you want to delete <br> <span class="fw-medium text-body">${product} from ${warehouse} warehouse</span> ?</p> <p class="text-warning" style="font-size: 12px">This will delete ${items} item(s).</p>`,
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Delete',
          cancelButtonText: 'Cancel',
          customClass: {
            confirmButton: 'btn btn-primary',
            cancelButton: 'btn btn-secondary'
          }
        }).then(result => {
          if (result.isConfirmed) {
            window.location.href = this.getAttribute('href'); //redirect to herf
          } else {
            Swal.fire({
              title: 'Cancelled',
              html: `<p>Did not delete <span class="fw-medium text-primary">${product}</span></p>`,
              icon: 'error',
              confirmButtonText: 'Ok',
              customClass: {
                confirmButton: 'btn btn-success'
              }
            });
          }
        });
      });
    });
  })();
});
