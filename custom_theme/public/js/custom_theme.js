window.onload = () => {
  const setPageHeadMargin = () => {
    if (document.getElementsByClassName("navbar").length > 0) {
      if (document.getElementsByClassName("navbar")[0].offsetHeight > 60) {
        $(".page-head").css("margin-top", "45px");
        $(".page-body").css("margin-top", "100px");
      } else {
        $(".page-head").css("margin-top", "0");
        $(".page-body").css("margin-top", "0");
      }
    }
  }

  const checkContentExist = () => {
    let isContentExist = setInterval(function () {
      if ($('.page-head').length) {
        setTimeout(() => {
          setPageHeadMargin();
        }, 250);
        clearInterval(isContentExist);
      }
    }, 100);
  }

  checkContentExist();
  frappe.route.on('change', () => {
    checkContentExist();
  });

  window.addEventListener("resize", ()=> {
    checkContentExist();
  });
}

frappe.ui.form.on('Custom Theme Setup', {
  refresh(frm) {
    cur_frm.add_custom_button(__("Install Icons"), function() {
      frappe.call({
        method: 'custom_theme.file_generator.install_theme_icon',        
        callback: function(response) {
          if (!response.exc) {
            frappe.msgprint("Go to your bench folder and run bench restart")
          }
        }
      });
    });
  },
  validate(frm) {
    frappe.call({
      method: 'custom_theme.file_generator.color_validation',
      args: {
        form_data: frm.doc
      },
      callback: function(response) {
        if (!response.exc) {
          const valid = response.message.valid;
          const message = response.message.message;
          if (!valid) {
            frappe.validated = false;
            frappe.throw(message);
          }
        }
      }
    });
  },
  after_save (frm) {
    frappe.call({
      method: 'custom_theme.file_generator.generate_css',
      args: {
        form_data: frm.doc
      },
      callback: function(response) {
        if (!response.exc) {
          frappe.msgprint(response.message);
        }
      }
    });
  }
})
