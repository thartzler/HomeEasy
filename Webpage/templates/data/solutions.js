$(document).ready(function(){
    
	// Define variables that reference our script tags within the body of our page
    var solutionTemp = $("#solutionTemplate").html();
    
	// Have MustacheJS render our script tags
	Mustache.parse(solutionTemp);

	var solutions = {
        solutions:
        [
            {
                name: "Electrical",
                link: "../product_reviews/electrical.html",
                qualifications: " Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus",
                icon: "fas fa-plug"
            },
            {
                name: "HVAC",
                link: "../product_reviews/hvac.html",
                qualifications: " Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus",
                icon: "fas fa-snowflake"
            },
            {
                name: "Plumbing",
                link: "../product_reviews/plumbing.html",
                qualifications: " Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus",
                icon: "fas fa-faucet",
            },
            {
                name: "Solar",
                link: "../product_reviews/solar.html",
                qualifications: " Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus",
                icon: "fas fa-solar-panel"
            },
            {
                name: "Networking",
                link: "../product_reviews/networking.html",
                qualifications: " Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus",
                icon: "fas fa-wifi",
            },
            {
                name: "Security",
                link: "../product_reviews/security.html",
                qualifications: " Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus",
                icon: "fas fa-key",
            },
            {
                name: "Smart Home",
                link: "../product_reviews/smart-home.html",
                qualifications: " Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus",
                icon: "fas fa-house-user",
            }
        ]
    };
    var renderedSolutions = Mustache.render(solutionTemp, solutions);
    $("#render_solutions").html(renderedSolutions);


	
});