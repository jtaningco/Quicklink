<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
    <meta property="og:image" content="./static/thumbnail.svg" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="www.quicklink.ph" />
    <meta property="og:title" content="Quicklink: Click your way to quick and easy transactions." />
    <meta property="og:description" content=" Quicklink automates order and financial processes, management, and documentation for small business owners to increase efficiency and return of sales." />
    <meta http-equiv="Cache-control" content="no-cache">
    <meta http-equiv="Expires" content="-1">

    <title>Quicklink: Early Access Form</title>
    <link rel="icon" href="static/logos/logo.png">
    
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="css/home.css">
    <link rel="stylesheet" href="css/form.css">

    <!-- JQUERY < 3.0.0 -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    
    <!-- ReCAPTCHA -->
    <script src="https://www.google.com/recaptcha/api.js" async defer></script>

    <!-- EmailJS -->
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/emailjs-com@2/dist/email.min.js"></script>
    <script type="text/javascript">
        emailjs.init('user_1xwNoD1h4pRrRQRCyHR8E')
    </script>
    <script src="js/form.js"></script>

    <!-- Local Scripts -->
    <script src="js/nav.js"></script>
</head>
<body>
    <nav class="navLanding">
        <div class="navWrapper scrolled" id="navbar">
          <div class="navBurger">
            <div class="burger burger-squeeze scroll" id="navBurger" style="font-size: 10px;">
              <div class="burger-lines" id="burgerLines"></div>
            </div>
          </div>
      
          <div class="navLinks" id="openMobileNav">
            <a class="logoLink" href="index.html"><div class="scrolled" id="navLogo"></div><img class="navMobileLogo" src="static/logos/logo.png"></a>
            <a class="navOptions mobileHome" href="index.html">Home</a>
            <a class="navOptions scrolled" href="how-it-works.html">How It Works</a>
            <a class="navOptions scrolled" href="pricing.html">Pricing</a>
            <a class="navOptions scrolled" href="faqs.html" active>FAQs</a>
    
            <!-- add link to all early access buttons-->
            <button class = "navMobileButton primary-btn"><a class = "navMobileButtonLink primary-btn-link">Join Early Access</a></button> 
          </div>
      
          <div class = "navButton">
            <button id="navButton" class="primary-btn"><a id="navButton-link" class="primary-btn-link">Join Early Access</a></button>
          </div>
        </div>
    </nav>

    <section class="earlyAccessForm">
        <div class="container">
            <div class="instructionsWrapper">
                <div class="sticky">
                        <h3 class="instructionsHeader body big bold">As a member of our early access program, you’ll be able to:</h3>
                        <div class="list">
                            <img src="./static/icons/check.svg" class="check">
                            <p class="body">Receive orders and payments</p>
                        </div>
                        <div class="list">
                            <img src="./static/icons/check.svg" class="check">
                            <p class="body">Document all your transactions</p>
                        </div>
                        <div class="list">
                            <img src="./static/icons/check.svg" class="check">
                            <p class="body">See your pending orders</p>
                        </div>
                        <div class="list">
                            <img src="./static/icons/check.svg" class="check">
                            <p class="body">Create and share your own order form</p>
                        </div>
                        <div class="list">
                            <img src="./static/icons/check.svg" class="check">
                            <p class="body">Get access to revenue reports</p>
                        </div>
                        <div class="instructionsEnding body big">
                            Want all these features for <span style="color: #FF8A00">FREE</span>? Fill out the form, and we’ll get back to you within 2-5 days!
                        </div>
                </div>
            </div>
            
            <div class="formContainer">
                <div class="formWrapper">
                    <div class="formContext">        
                        <h2 class="formTitle bold">Be one of our first merchants!</h2>
                        <p class="body">Filling out this form will help us prepare for your use of Quicklink's early access program! Expect an email within 2-5 days from a team member.</p>
                    </div>
                    <form method="POST" id="my-form">
                        <div class="formItem">
                            <label class="body bold">What's your name?<span style="color: #F35252">*</span></label>
                            <input class="form-field" type="text" placeholder="Name" name="name" required>
                        </div>
        
                        <div class="formItem">
                            <label class="body bold">Can I get your email address?<span style="color: #F35252">*</span></label>
                            <input class="form-field" type="text" placeholder="Email Address" name="_replyto" required>
                        </div>

                        <div class="formItem">
                            <label class="body bold">How about your mobile number?<span style="color: #F35252">*</span></label>
                            <input class="form-field" type="text" placeholder="Mobile Number" name="number" required>
                        </div>

                        <div class="formItem">
                            <label class="body bold">What's your shop's name?<span style="color: #F35252">*</span></label>
                            <input class="form-field" type="text" placeholder="Shop Name" name="shop" required>
                        </div>

                        <div class="formItem">
                            <label class="body bold">What link/s can we use to find your shop?<span style="color: #F35252">*</span></label>
                            <input class="form-field" type="text" placeholder="Shop Link" name="link" required>
                        </div>

                        <div class="formItem">
                            <label class="body bold">Can you quickly describe your shop?<span style="color: #F35252">*</span></label>
                            <Textarea class="textarea subtitle form-field" placeholder="Shop Description" name="description"></Textarea>
                        </div>

                        <div class="formItem">
                            <label class="body bold">On average, how many customers you have in a month?<span style="color: #F35252">*</span></label>
                            <input class="form-field" type="text" placeholder="No. of Customers" name="customers" required>
                        </div>

                        <div class="formItem">
                            <label class="body bold">Where are you based?<span style="color: #F35252">*</span></label>
                            <input class="form-field" type="text" placeholder="Location" name="location" required>
                        </div>

                        <div class="formItem">
                            <label class="body bold">How did you hear about us?<span style="color: #F35252">*</span></label>
                            <input class="form-field" type="text" placeholder="Referral? Facebook? Instagram?" name="find" required>
                        </div>

                        <!-- ReCaptcha -->
                        <!-- <div class="formItem">
                            <div class="g-recaptcha" data-sitekey="6LfySloaAAAAACZEAph0oFmuXhc2-LNrjUUAdB3v"></div>
                        </div> -->
        
                        <button type="submit" formmethod="POST" class="primary-btn disabled submitForm" id="confirmButton">
                            <p id="confirm" class="primary-btn-link disabled submitFormLink">Request for Early Access</p>
                        </button>
                    </form>
                </div>
            </div>

            <img src="./static/background/formEllipse6.png" id="big-circle">
            <img src="./static/background/formEllipse7.png" id="small-circle">
        </div>
    </section>
    <script>
        $(".form-field").on("keyup", function () {    	
            canChangeColor();
        });
        
        
        function canChangeColor(){          
            var can = true;  
            $(".form-field").each(function(){
            if($(this).val()==''){
                can = false;
            }
            });
            
            if(can){
                $('#confirmButton').toggleClass('disabled', false)
                $('#confirm').toggleClass('disabled', false)
            } else {
                $('#confirmButton').toggleClass('disabled', true)
                $('#confirm').toggleClass('disabled', true)
            }
        }
    </script>
</body>
</html>