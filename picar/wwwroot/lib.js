function line(direction, speed) {
    data.motor.A.direction = direction;
    data.motor.B.direction = direction;
    data.motor.A.speed = speed;
    data.motor.B.speed = speed;
}

function left(speed) {
    data.motor.A.direction = 1;
    data.motor.B.direction = 0;
    data.motor.A.speed = speed;
    data.motor.B.speed = speed;
}

function right(speed) {
    data.motor.A.direction = 0;
    data.motor.B.direction = 1;
    data.motor.A.speed = speed;
    data.motor.B.speed = speed;
}

function fore(speed) {
    line(0, speed);
}

function back(speed) {
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