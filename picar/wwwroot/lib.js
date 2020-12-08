function line(direction, speed=10) {
    data.motor.A.direction = direction;
    data.motor.B.direction = direction;
    data.motor.A.speed = speed;
    data.motor.B.speed = speed;
}

function left(speed=10) {
    data.motor.A.direction = 1;
    data.motor.B.direction = 0;
    data.motor.A.speed = speed;
    data.motor.B.speed = speed;
}

function right(speed=10) {
    data.motor.A.direction = 0;
    data.motor.B.direction = 1;
    data.motor.A.speed = speed;
    data.motor.B.speed = speed;
}

function fore(speed=10) {
    line(0, speed);
}

function back(speed=10) {
    line(1, speed);
}

function stop() {
    line(0, 0);
}

function color(id, value) {
    let r = parseInt(value.substring(1, 3), 16);
    let g = parseInt(value.substring(3, 5), 16);
    let b = parseInt(value.substring(5, 7), 16);
    data.led.leds[id] = [r, g, b, 0];
}

function irup(speed = 10) {
    data.controller.ir_up = {
        speed: speed
    }
}

function irdown() {
    data.controller.ir_down = [true];
}

function stup(start = null, diff = 100, speed = 10, interval = 0.1) {
    data.controller.st_up = {
        diff: diff,
        speed: speed,
        interval: interval
    }
    if (start != null) {
        data.st_up.start = start
    }

}

function stdown() {
    data.controller.st_down = [true];
}