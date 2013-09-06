
// Toggle select checkboxes within a form using a single checkbox

function toggleSelect(FormId, ControllerId, FieldId)
{
  if(!document.forms[FormId])
    return;
    
  var objController = document.forms[FormId].elements[ControllerId];
  var objCheckBoxes = document.forms[FormId].elements[FieldId];
  
  if(!objCheckBoxes)
    return;
  
  var countCheckBoxes = objCheckBoxes.length;
  
  if(!countCheckBoxes)
    objCheckBoxes.checked = objController.checked;
  else
    for(var i = 0; i < countCheckBoxes; i++)
      if(objCheckBoxes[i].disabled == false)
        objCheckBoxes[i].checked = objController.checked;
}

// Show-hide parts of form

function toggleForm() {
    var e, i = 0;
    while (e = document.getElementById('gallery').getElementsByTagName ('B') [i++]) {
        if (e.className == 'switch') {
        e.onclick = function () {
            var getEls = document.getElementById('gallery').getElementsByTagName('DIV');
                for (var z=0; z<getEls.length; z++) {
                if (getEls[z].className == 'hide') {
                w=getEls[z].previousSibling;
                while (w.nodeType!=1) {
                    w=w.previousSibling;
                    }
                w.className=w.className.replace('switch over', 'switch');
                }
                if (getEls[z].className == 'show') {
                getEls[z].className=getEls[z].className.replace('show', 'hide');
                w=getEls[z].previousSibling;
                while (w.nodeType!=1) {
                    w=w.previousSibling;
                    }
                w.className=w.className.replace('switch off', 'switch over');
                }
            }
            this.className = this.className == 'switch' ? 'switch off' : 'switch';
            x=this.nextSibling;
            while (x.nodeType!=1) {
                x=x.nextSibling;
                }
            x.className = this.className == 'switch off' ? 'show' : 'hide';
            }
        }
    }
}

// Check validity of inputs within the Password form

function checkPwdForm() {
  var elem = document.getElementById("password");
  var pwd1 = elem.value;
  var pwd2 = document.getElementById("confirm").value;
  var user = document.getElementById("id").value;
  
  if(pwd1 != "" && pwd1 == pwd2) {
    if(pwd1.length < 6) {
      msg("Error: Password must contain at least six characters");
      elem.select();
      elem.focus();
      return false;
    }
    if(pwd1 == user) {
      msg("Error: Password must be different from user name");
      elem.select();
      elem.focus();
      return false;
    }
    
    re = /[0-9]/;
    if(!re.test(pwd1)) {
      msg("Error: password must contain at least one number (0-9)");
      elem.select();
      elem.focus();
      return false;
    }
  }
  else {
    msg("Error: Please check that you've entered and confirmed your password");
    elem.select();
    elem.focus();
    return false;
  }
  return true;
}

// Display error message associated with an incorrect password response (called from checkPwdForm)

function msg(message) {
  var emptyString = /^\s*$/ ;
  var dispmessage;
  if (emptyString.test(message)) {
    dispmessage = String.fromCharCode(nbsp);
  }
  else {
    dispmessage = message;
  }
  document.getElementById("msg").innerHTML = dispmessage;
}

// Check validity of inputs within the Registration form

function checkRegForm() {
  var email = document.getElementById("email").value;
  var fname = document.getElementById("fname").value;
  var lname = document.getElementById("lname").value;
  
  if (email == "" || validateEmail(email)) {
    hideAllErrors();
    document.getElementById("emailError").style.display = "inline";
    document.getElementById("email").select();
    document.getElementById("email").focus();
    return false;
  }
  else if (fname == "") {
    hideAllErrors();
    document.getElementById("fnameError").style.display = "inline";
    document.getElementById("fname").select();
    document.getElementById("fname").focus();
    return false;
  }
  else if (lname == "") {
    hideAllErrors();
    document.getElementById("lnameError").style.display = "inline";
    document.getElementById("lname").select();
    document.getElementById("lname").focus();
    return false;
  }
  return true;
}

// Hide error messages in Registration form

function hideAllErrors() {
  document.getElementById("emailError").style.display = "none"
  document.getElementById("fnameError").style.display = "none"
  document.getElementById("lnameError").style.display = "none"
}

// Validate email address

function validateEmail(fld) {
  var tfld = trim(fld);
  var emailFilter = /^[^@]+@[^@.]+\.[^@]*\w\w$/ ;
  var illegalChars= /[\(\)\<\>\,\;\:\\\"\[\]]/ ;
  if (!emailFilter.test(tfld) || fld.match(illegalChars)) {
    return true;
  }
  return false;
}

// Trim whitespace at start and end of string

function trim(s) {
  return s.replace(/^\s+|\s+$/, '');
}

// Confirm submit pop-up with dialog box

function confirmSubmit() {
var agree=confirm("Are you sure you wish to continue?");
if (agree)
  return true ;
else
  return false ;
}

// Set forms default focus given field id

function setDefaultFocus(FieldId) {
  document.getElementById(FieldId).focus();
}

