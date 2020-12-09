function randint(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

function line(direction) {
    data.motor.A.direction = direction;
    data.motor.B.direction = direction;
}

function left() {
    data.motor.A.direction = 1;
    data.motor.B.direction = 0;
}

function right() {
    data.motor.A.direction = 0;
    data.motor.B.direction = 1;
}

function fore() {
    line(0);
}

function back() {
    line(1);
}

function speed(speed = 10) {
    data.motor.A.speed = speed;
    data.motor.B.speed = speed;
}

function stop() {
    speed(0);
}

function speedup(speed = 10) {
    data.motor.A.speed += speed;
    data.motor.B.speed += speed;
}

function speeddown(speed = 10) {
    data.motor.A.speed -= speed;
    data.motor.B.speed -= speed;
}

function color(id, value) {
    let r = parseInt(value.substring(1, 3), 16);
    let g = parseInt(value.substring(3, 5), 16);
    let b = parseInt(value.substring(5, 7), 16);
    data.led.leds[id] = [r, g, b, 255];
}

function randcolor(id = null) {
    if (id == null) {
        for (let i = 0; i < 4; i++) {
            randcolor(i);
        }
    }
    else {
        let r = randint(0, 256);
        let g = randint(0, 256);
        let b = randint(0, 256);
        data.led.leds[id] = [r, g, b, 255];
    }
}

function randclosecolor(id = null, delta = 10) {
    if (id == null) {
        for (let i = 0; i < 4; i++) {
            randclosecolor(i);
        }
    }
    else {
        let fr = randint(0, 2);
        let fg = randint(0, 2);
        let fb = randint(0, 2);
        let r = Math.max(0, Math.min(255, data.led.leds[id][0] + (fr == 0 ? -1 : 1) * delta));
        let g = Math.max(0, Math.min(255, data.led.leds[id][1] + (fg == 0 ? -1 : 1) * delta));
        let b = Math.max(0, Math.min(255, data.led.leds[id][2] + (fb == 0 ? -1 : 1) * delta));
        data.led.leds[id] = [r, g, b, 255];
    }
}

function irup(speed = 10) {
    data.controller.ir_up = {
        speed: speed
    }
}

function irdown() {
    data.controller.ir_down = [true];
}

function stup(start = null, diff = 500, speed = 10, interval = 0.3) {
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
