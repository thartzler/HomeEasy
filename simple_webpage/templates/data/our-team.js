$(document).ready(function(){
    
	// Define variables that reference our script tags within the body of our page
    var employeeFormat = $("#employeeTemplate").html();
    
	// Have MustacheJS render our script tags
	Mustache.parse(employeeFormat);

	var employees = {
        employee:
        [
            {
                image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRaVN5c6APRWyAHOR--cKN8TD3iSdX5n2NjjQ&usqp=CAU",
                altText: "Employee1 Photo",
                name: "Jeff Hartzler",
                title: "President",
                division: "Founder",
                text: "Jeff worked as an electrician for 20 years before starting Hartzler Home Solutions. It was always his dream to someday be able to lead an incredible team to provide customers with the best solutions for updating and repairing your home."
            },
            {
                image: "https://i.pinimg.com/originals/49/2a/09/492a09cb4fa485bbacca9e08db7e2680.jpg",
                altText: "Employee2 Photo",
                name: "Donna Hartzler",
                title: "Lead",
                division: "Reception/Accounting",
                text: "Donna has been married to Jeff for 15 year and worked at Hartzler Home Solutions since the beginning. While not at work, Donna is taking care of their 4 kids. She makes the best lasagna in the state."
            },
            {
                image: "https://thumbs.dreamstime.com/b/female-resort-receptionist-working-front-desk-female-resort-receptionist-working-front-desk-123116005.jpg",
                altText: "Employee3 Photo",
                name: "Sally Natt",
                title: "Solution Assistant",
                division: "Reception",
                text: "Sally is probably the chearful voice you will probably hear when you call our office. She has an incredible talent and intuitiion when it comes to crafting solutions for our customers. Prepare to be impressed when you first speak with Sally."
            },
            {
                image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCgIWd-4OLVVeNjOEHRJQWcY9ZUN144m1dIQ&usqp=CAU",
                altText: "Employee4 Photo",
                name: "Theo Marsh",
                title: "Solution Master",
                division: "Plumbing",
                text: "Theo has been a master plumber for over 25 years. He can fix any toilet or leaky pipe without hardly looking at it. He is father to a son and 2 daughters and 5 grandchildren."
            },
            {
                image: "https://cdn.pixabay.com/photo/2017/09/16/14/33/electrician-2755686__340.jpg",
                altText: "Employee5 Photo",
                name: "Max Thomson",
                title: "Solution Master",
                division: "Electrical",
                text: "Max is a very hardworking man who appreciated a well organized jobsite. He's been with HHS since the beginning and continues to teach us all every day."
            },
            {
                image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-Zu3IlW4OoFQqgP__2FtT5qJvu2hFKE5uew&usqp=CAU",
                altText: "Employee6 Photo",
                name: "Drew Humphry",
                title: "Solution Provider",
                division: "Solar",
                text: "Drew has been with the company for 8 years and is know for his famous chocolate chip cookies. He also has a special talent to be able to pull electrons from the sky."
            },
            {
                image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-Zu3IlW4OoFQqgP__2FtT5qJvu2hFKE5uew&usqp=CAU",
                altText: "Employee7 Photo",
                name: "Brandon Poll",
                title: "Solution Provider",
                division: "Solar",
                text: "Drew has been with the company for 8 years and is know for his famous chocolate chip cookies. He also has a special talent to be able to pull electrons from the sky."
            },
            {
                image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-Zu3IlW4OoFQqgP__2FtT5qJvu2hFKE5uew&usqp=CAU",
                altText: "Employee8 Photo",
                name: "Drew Humphry",
                title: "Solution Provider",
                division: "Solar",
                text: "Drew has been with the company for 8 years and is know for his famous chocolate chip cookies. He also has a special talent to be able to pull electrons from the sky."
            }
        ]
    };
    var renderedEmployees = Mustache.render(employeeFormat, employees);
    $("#render_employees").html(renderedEmployees);


	
});