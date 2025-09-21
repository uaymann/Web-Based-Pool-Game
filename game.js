$(document).ready(function() {
    var drawing = false; // Flag to check if we are currently drawing
    var cueBallCenter = { x: 0, y: 0 }; // Variable to store the center position of the cue ball
    var timer; // Variable to store the timer
    var curr = 0; // Start with the first SVG
    var allSvgs = $('#svgContainer svg').length;
    //var svgArray = svgData.split('|').filter(Boolean);

    $('#svgContainer svg').hide().first().show();

    function animation() {
        curr++; // Move to the next SVG
        if (curr >= allSvgs) {
            clearInterval(animationTimer); // Stop the animation after the last SVG
            if (window.location.pathname.includes("animate.html")) {
                window.location.href = 'index.html';
            }
            return; // Exit the function
        }
        $('#svgContainer svg').hide(); // Hide all SVGs
        $('#svgContainer svg').eq(curr).show(); // Show current SVG
        
        return;
    }

    // Set the timer for 15 seconds
    timer = setTimeout(function() {
        if (window.location.pathname.includes("animate.html")) {
            // Fade out the page
            $('body').fadeOut(1000, function() {
                // Redirect to index.html after fading out
                window.location.href = 'index.html';
            });
        }
    }, 15000); // 15 seconds

    // Start the animation timer
    var animationTimer = setInterval(animation, 50);


    $(document).mousedown(function(event) {
        // Start drawing
        drawing = true;
        $('#line').show();  

        // Draw line from cue ball center to current mouse position
        drawLine(event);

    });


    $(document).mouseup(function(event) {
        
        if (drawing) {
            drawing = false;
            $('#line').hide(); // Hide the line
            
            var mouseX = event.pageX * 2 - 25;
            var mouseY = event.pageY * 2 - 25;


            // Get the center position of the cue ball
            var cueBall = $('circle[fill="WHITE"]');

            var cueBallCX = parseFloat(cueBall.attr('cx'));
            var cueBallCY = parseFloat(cueBall.attr('cy'));

            cueBallCenter = { 
                x: cueBallCX, 
                y: cueBallCY
            };
            // Print or use the initial velocity as needed
            // Calculate velocity
            var dx = mouseX - cueBallCenter.x;
            var dy = mouseY - cueBallCenter.y;
            var scale_factor = 10;

            var velocity_x = dx * scale_factor;
            var velocity_y = dy * scale_factor;
            console.log("x velocity:", velocity_x);
            console.log("y velocity:", velocity_y);
          
            // Here we send the initial velocity to your server
            // Send velocity data to server using AJAX POST
            $.ajax({
                type: "POST",
                url: '/send', // Replace with your server URL
                contentType: "application/json",
                data: JSON.stringify({ velocity_x: velocity_x, velocity_y: velocity_y }),
            });
            console.log("sucess", velocity_x)
            //window.location.href = 'animate.html';
            $.ajax({
                type: "GET",
                url: 'animate.html',
                success: function(data) {
                    if (data.trim().length > 0) {
                        console.log("animate.html woohoo");
                        window.location.href = 'animate.html';
                    } else {
                        console.log("animate.html is empty");
                        // Handle the case when animate.html is empty
                    }
                },
                error: function(xhr, status, error) {
                    console.error("Error fetching animate.html:", error);
                }
            });
            
            setTimeout(function() {
                $(document).ready();
            }, 500); // Adjust the delay time as needed
        }
    });

    $(document).mousemove(function(event) {
        // If we are drawing (mouse is pressed down), update the line
        if (drawing) {
            // Update line from cue ball center to current mouse position
            drawLine(event);
        }
    });
  
    function drawLine(event) {
        var mouseX = event.pageX * 2 - 25;
        var mouseY = event.pageY * 2 - 25;

        // Get the center position of the cue ball
        var cueBall = $('circle[fill="WHITE"]');

        var cueBallCX = parseFloat(cueBall.attr('cx'));
        var cueBallCY = parseFloat(cueBall.attr('cy'));

        cueBallCenter = { 
            x: cueBallCX, 
            y: cueBallCY
        };
  
        $('#line').attr({
            'x1': cueBallCX,
            'y1': cueBallCY,
            'x2': mouseX,
            'y2': mouseY
        });

        // Log the line and its coordinates
        console.log("Line coordinates:");
        console.log("x1:", cueBallCX);
        console.log("y1:", cueBallCY);
        console.log("x2:", mouseX);
        console.log("y2:", mouseY);
    }

});
