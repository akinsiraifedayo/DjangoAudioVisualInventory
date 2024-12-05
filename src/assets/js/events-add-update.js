'use strict';

document.addEventListener('DOMContentLoaded', function (e) {
  (function () {
    // Variables for DataTable
    var WarehouseName = $('#transaction-date');
    var DueDate = $('#due-date');
    var select2 = $('.select2');

    if (select2.length) {
      select2.each(function () {
        var $this = $(this);
        $this.wrap('<div class="position-relative"></div>    ').select2({
          placeholder: 'Click to Select',
          dropdownParent: $this.parent()
        });
      });
    }

    // Transaction Date (flatpicker)
    // if (WarehouseName) {
    //   WarehouseName.flatpickr({
    //     monthSelectorType: 'static',
    //     altInput: true,
    //     altFormat: 'M j, Y'
    //     // dateFormat: 'Y-m-d'
    //   });
    // }

    // DueDate (flatpicker)
    
    const addWarehouseForm = document.getElementById('addWarehouseForm');
    if (addWarehouseForm) {
      // Add New Customer Form Validation
      const fv = FormValidation.formValidation(addWarehouseForm, {
        fields: {
          name: {
            validators: {
              notEmpty: {
                message: 'Please enter Warehouse Name'
              }
            }
          },
          location: {
            validators: {
              notEmpty: {
                message: 'Please enter Warehouse Location'
              }
            }
          },
          products: {
            validators: {
              notEmpty: {
                message: 'Please select Warehouse Products'
              }
            }
          },
          contact_person: {
            validators: {
              notEmpty: {
                message: 'Please select Warehouse Contact Person'
              }
            }
          },
          email: {
            validators: {
              notEmpty: {
                message: 'Please enter contact person email'
              }
            }
          },
          phone: {
            validators: {
                notEmpty: {
                    message: 'Please enter a phone number'
                },
                regexp: {
                    regexp: /^\+?[0-9]{10,}$/,
                    message: 'Please enter a valid phone number'
                }
            }
          },
        },
        plugins: {
          trigger: new FormValidation.plugins.Trigger(),
          bootstrap5: new FormValidation.plugins.Bootstrap5({
            eleValidClass: '',
            rowSelector: '.mb-3'
          }),
          submitButton: new FormValidation.plugins.SubmitButton(),

          defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
          autoFocus: new FormValidation.plugins.AutoFocus()
        },
        init: instance => {
          instance.on('plugins.message.placed', function (e) {
            if (e.element.parentElement.classList.contains('input-group')) {
              e.element.parentElement.insertAdjacentElement('afterend', e.messageElement);
            }
          });
        }
      });
    }

    // update transaction form validation

    const UpdateWarehouseForm = document.getElementById('UpdateWarehouseForm');
    if (UpdateWarehouseForm) {
      const fv = FormValidation.formValidation(UpdateWarehouseForm, {
        fields: {
          name: {
            validators: {
              notEmpty: {
                message: 'Please enter Warehouse Name'
              }
            }
          },
          location: {
            validators: {
              notEmpty: {
                message: 'Please enter Warehouse Location'
              }
            }
          },
          products: {
            validators: {
              notEmpty: {
                message: 'Please select Warehouse Products'
              }
            }
          },
          contact_person: {
            validators: {
              notEmpty: {
                message: 'Please select Warehouse Contact Person'
              }
            }
          },
          email: {
            validators: {
              notEmpty: {
                message: 'Please enter contact person email'
              }
            }
          },
          phone: {
            validators: {
              notEmpty: {
                message: 'Please enter contact person phone'
              },
              regexp: {
                regexp: /^\+?[0-9]{10,}$/,
                message: 'Please enter a valid phone number'
              }
            }
          },
        },
        plugins: {
          trigger: new FormValidation.plugins.Trigger(),
          bootstrap5: new FormValidation.plugins.Bootstrap5({
            eleValidClass: '',
            rowSelector: '.mb-3'
          }),
          submitButton: new FormValidation.plugins.SubmitButton(),

          defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
          autoFocus: new FormValidation.plugins.AutoFocus()
        },
        init: instance => {
          instance.on('plugins.message.placed', function (e) {
            if (e.element.parentElement.classList.contains('input-group')) {
              e.element.parentElement.insertAdjacentElement('afterend', e.messageElement);
            }
          });
        }
      });
    }
  })();
});
