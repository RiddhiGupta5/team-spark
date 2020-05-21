window.onload = function () {

  //WELCOME USER    @Done
  let token = localStorage.getItem("token");
  fetch("https://crack-corona-hack-backend.herokuapp.com/app/user/details/", {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
  })
    .then(res => {
      return res.json()
    })
    .then(res => {
      if (res.message === "User details") {
        document.getElementById("welcome").innerHTML = res.User.username;
      } else {

      }
    })
    .catch(err => {
      console.log(err);
    })

  // -----------------------------------------------------------------------------------------------------------------------

  //ADD DONATIONS JS  @Done

  document.getElementById("sub").addEventListener("click", function (e) {

    var itemname = document.getElementById("itemname").value;
    var quantity = document.getElementById("quantity").value;
    var description = document.getElementById("desc").value;


    let status = [];


    if (itemname.length <= 1) {
      document.getElementById("itemname").style.borderColor = "red";
      document.getElementById("itemname").value = "";
      document.getElementById("itemname").placeholder = "Please enter valid item name";
      status.push("false")
      document.getElementById("itemname").classList.add("red");
    } else {
      status.push("true")
    }
    if (quantity.length < 1) {
      document.getElementById("quantity").style.borderColor = "red";
      document.getElementById("quantity").value = "";
      document.getElementById("quantity").placeholder = "Please enter valid quantity";
      status.push("false")
      document.getElementById("quantity").classList.add("red");
    } else {
      status.push("true")
    }
    if (description.length <= 1) {
      document.getElementById("desc").style.borderColor = "red";
      document.getElementById("desc").value = "";
      document.getElementById("desc").placeholder = "Please enter valid description";
      status.push("false")
      document.getElementById("desc").classList.add("red");
    } else {
      status.push("true")
    }
    if (status.includes("false")) {
      console.log("There was some error while validating")
      return false
    }
    else {
      console.log("Validated")
      document.getElementById("sub").value = "Loading..."
      let token = (localStorage.getItem("token"));
      fetch("https://crack-corona-hack-backend.herokuapp.com/app/donation/", {
        method: 'POST',
        headers: new Headers({
          'content-type': 'application/json',
          'Authorization': `Bearer ${token}`
        }),
        body: JSON.stringify({
          item_name: itemname,
          quantity: quantity,
          description: description
        }),
      })
        .then(res => {
          return res.json()
        })
        .then(res => {
          if (res.message.id) {
            document.getElementById("banner").style.backgroundColor = "green";
            document.getElementById("banner").style.display = "block";
            document.getElementById("banner").innerHTML = "You donation request has been submitted!!";
            document.getElementById("banner").classList.add("error");
            document.getElementById("sub").value = "Submit";
            setTimeout(() => {
              window.location.href = "donors.html";
            }, 2500)
          } else if (res.err == "User already exist") {
            document.getElementById("banner").style.backgroundColor = "red";
            document.getElementById("banner").style.display = "block";
            document.getElementById("banner").innerHTML = "User already exist!! Try signing in."
            document.getElementById("banner").classList.add("error");
            document.getElementById("sub").value = "Submit"
          } else {
            document.getElementById("banner").style.backgroundColor = "red";
            document.getElementById("banner").style.display = "block";
            document.getElementById("banner").innerHTML = "Unexpected error occurred"
            document.getElementById("banner").classList.add("error");
            document.getElementById("sub").value = "Submit"
          }
        })
        .catch(err => {
          document.getElementById("banner").style.backgroundColor = "red";
          document.getElementById("banner").style.display = "block";
          document.getElementById("banner").innerHTML = "It's on us! There was some error"
          document.getElementById("banner").classList.add("error");
          document.getElementById("sub").value = "Submit"
        })
    }
  });

  // -----------------------------------------------------------------------------------------------------------------------

  //LOGOUT JS  @Done

  document.getElementById("logout").addEventListener("click", function (e) {
    e.preventDefault()
    let token = localStorage.getItem("token");
    fetch("https://crack-corona-hack-backend.herokuapp.com/app/user/logout", {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
    })
      .then(res => {
        return res.json()
      })
      .then(res => {
        console.log(res)
        if (res.message === "User logged out") {
          document.getElementById("banner").style.backgroundColor = "green";
          document.getElementById("banner").style.display = "block";
          document.getElementById("banner").innerHTML = "You have successfully logged out!";
          document.getElementById("banner").classList.add("error");
          setTimeout(() => {
            window.location.href = "index.html";
          }, 2500)
        } else {
          document.getElementById("banner").style.backgroundColor = "red";
          document.getElementById("banner").style.display = "block";
          document.getElementById("banner").innerHTML = "You have already logged out"
          document.getElementById("banner").classList.add("error");
        }
      })
      .catch(err => {
        console.log(err)
        document.getElementById("banner").style.backgroundColor = "red";
        document.getElementById("banner").style.display = "block";
        document.getElementById("banner").innerHTML = "It's on us! There was some error"
        document.getElementById("banner").classList.add("error");
      })
  });

  // -----------------------------------------------------------------------------------------------------------------------

  //VIEW PROFILE JS  @Done

  document.getElementById("profile").addEventListener("click", function (e) {
    e.preventDefault()
    let token = localStorage.getItem("token");
    fetch("https://crack-corona-hack-backend.herokuapp.com/app/user/details/", {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
    })
      .then(res => {
        return res.json()
      })
      .then(res => {

        if (res.message === "User details") {
          document.getElementById("pr_nameofuser").innerHTML = res.User.username;
          document.getElementById("pr_location").innerHTML = res.User.address;
          document.getElementById("pr_email").innerHTML = res.User.email;
          document.getElementById("pr_phone").innerHTML = res.User.phone_no;
        } else {

        }
      })
      .catch(err => {
        console.log(err);
      })
  })

  // -----------------------------------------------------------------------------------------------------------------------

  // VIEW DONATIONS JS

  document.getElementById("viewdonationjs").addEventListener("click", function getData(e) {
    let token = localStorage.getItem("token");
    fetch("https://crack-corona-hack-backend.herokuapp.com/app/all_donations/", {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
    })
      .then(res => {
        return res.json()
      })
      .then(res => {

        if (res.message === "Donations Found") {

          console.log(res);
          let content = "";
          let serial = 0;
          res.Donations.forEach(ele => {
            let itemname = ele.item_name;
            let quantity = ele.quantity;
            let description = ele.description;
            serial = serial + 1;
            content = content + `<div class="card" id="viewdonationcards">
            <h5 class="card-header" style="background-color: gainsboro; color: #f77f00" id="nameofitem">Item Name : ${itemname}</h5>
            <div class="card-body">
              <p class="card-text">
              <div style="font-size: 18px; font-weight: bolder; padding-bottom: 10px;" id="quanofitem"> Quantity: ${quantity}</div>
              <div style="font-size: 18px;font-weight: bolder;" id="descofitem"> Description: ${description}</div>
              </p>
            </div>
          </div>`
          })

          document.getElementById('viewdonationcards').innerHTML = content;

        }
      })
      .catch(err => {
        console.log(err);
      })
  })

  // -----------------------------------------------------------------------------------------------------------------------

  // VIEW HELP PROGRAMS JS

  document.getElementById("donor_help_programs").addEventListener("click", function (e) {
    e.preventDefault()
    fetch("https://crack-corona-hack-backend.herokuapp.com/app/all_help_prg/", {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(res => {
        return res.json()
      })
      .then(res => {

        if (res.message === "Help Programs Found") {
          console.log(res);
          let content = "";
          let serial = 0;
          res.HelpPrograms.forEach(ele => {
            let prgname = ele.prg_name;
            let orgname = ele.org_name;
            let aidprovided = ele.aid_provided;
            let city = ele.city;
            let address = ele.address;
            let description = ele.description;
            serial = serial + 1;
            content = content + `
            <div class="card" style="padding:5px" id="viewhelpprograms">
            <div class="card-body">
                <h5 class="card-title" style="color:#f77f00; font-weight:bolder">Programme name: ${prgname}</h5>
                <p class="card-text">
                <div style="font-size: 18px; font-weight: bolder; padding-bottom: 10px;" id="quanofitem"> Aid Provided:  ${aidprovided}</div>
                <div style="font-size: 18px; font-weight: bolder; padding-bottom: 10px;" id="quanofitem">Description:  ${description}</div>
                <div style="font-size: 18px; font-weight: bolder; padding-bottom: 10px;" id="quanofitem">City:  ${city}</div>
                <div style="font-size: 18px; font-weight: bolder; padding-bottom: 10px;" id="quanofitem">Address:  ${address}</div>
                </p>
            </div>
            <div class="card-body" style="background-color:grey; color:white" >
                <a href="#" class="card-link"> Org name: ${orgname}</a>
            </div>
        </div>`
          })

          document.getElementById('viewhelpprogrammes').innerHTML = content;

        } else {

        }
      })
      .catch(err => {
        console.log(err);
      })


  })

  //----------------------------------------------------------------------------------------------------------------------------------

  // VIEW MESSAGES JS

  document.getElementById("viewmessage").addEventListener("click", function (e) {
    e.preventDefault()
    let token = localStorage.getItem("token");
    fetch("https://crack-corona-hack-backend.herokuapp.com/app/view_messages/", {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
    })
      .then(res => {
        return res.json()
      })
      .then(res => {

        if (res.message === "Donations found") {
          console.log(res);
          let content = "";
          let serial = 0;
          res.Donations.forEach(ele => {
            let itemname = ele.item_name;
            let orgname = ele.org_name;
            let message = ele.message;
            serial = serial + 1;
            content = content + `<div class="media text-muted pt-3" style="width:100%; " id="messageinbox">
            <div class="mr-2 rounded" style="width:32; height:32"> ${serial} </div>
            <p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
              <strong class="d-block text-gray-dark" style="color:black;font-size:15px;">Organization Name: ${orgname}</strong>
              <strong class="d-block text-gray-dark" style="font-size:13px; color: #f77f00">Item Name: ${itemname}</strong>
              ${message}
            </p>
          </div>
          `
          })

          document.getElementById('messageinbox').innerHTML = content;

        }
      })
      .catch(err => {
        console.log(err);
      })
  })


};