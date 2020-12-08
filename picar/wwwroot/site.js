const App = {
    data() {
        return {
            led: {
                brightness: 128,
                leds: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
            },
            irsensor: {
                left: 0,
                right: 0,
                analog: [0, 0, 0, 0]
            },
            motor: {
                A: {
                    direction: 0,
                    speed: 0,
                },
                B: {
                    direction: 0,
                    speed: 0,
                }
            },
            model: {
                led: {
                    brightness: 128,
                    leds: [[255, 255, 255, 0], [255, 255, 255, 0], [255, 255, 255, 0], [255, 255, 255, 0]]
                },
                motor: {
                    A: 0,
                    B: 0,
                },
            }
        }
    },
    methods: {
        getLedColor(id) {
            let value = this.led.leds[id];
            let s = "#";
            for (let i = 0; i < 3; i++) {
                s += value[i].toString(16).padStart(2, "0")
            }
            return s;
        },
        getModelLedColor(id) {
            let value = this.model.led.leds[id];
            let s = "#";
            for (let i = 0; i < 3; i++) {
                s += value[i].toString(16).padStart(2, "0")
            }
            return s;
        },
        setModelLedColor(id, value) {
            let r = parseInt(value.substring(1, 3), 16);
            let g = parseInt(value.substring(3, 5), 16);
            let b = parseInt(value.substring(5, 7), 16);
            this.model.led.leds[id] = [r, g, b, 0];
            this.runOnce(`data.led.leds[${id}] = [${r},${g},${b},0]; return data;`);
        },
        run(rawCode) {
            try {
                let func = Function("data", rawCode);

                window.userFunc = func;
            } catch (error) {
                alert(error);
            }
        },
        runOnce(rawCode) {
            async function getData() {
                let data = await fetch('/api/').then(res => res.json());
                return data;
            }

            try {
                let func = Function("data", rawCode);

                getData().then(data => {
                    try {
                        let ret = func(JSON.parse(JSON.stringify(data)));
                        if (ret) {
                            this.post(ret);
                        }
                    } catch (error) {
                        alert(error);
                    }
                });
            } catch (error) {
                alert(error)
            }
        },
        onCompile(event) {
            try {
                let code = editor.getValue();
                func = Function("data", code);

                console.log("compiled")
            } catch (error) {
                alert(error)
            }
        },
        onRun(event) {
            this.run(editor.getValue());
        },
        onRunOnce(event) {
            this.runOnce(window.editor.getValue());
        },
        onStop(event) {
            window.userFunc = null;
        },
        onApplyLedBrightness(event) {
            this.runOnce(`data.led.brightness = ${this.model.led.brightness}; return data;`);
        },
        onApplyMotorA(event) {
            if (this.model.motor.A >= 0) {
                this.runOnce(`data.motor.A.direction = 1; data.motor.A.speed = ${this.model.motor.A}; return data;`);
            }
            else {
                this.runOnce(`data.motor.A.direction = 0; data.motor.A.speed = ${-this.model.motor.A}; return data;`);
            }
        },
        onApplyMotorB(event) {
            if (this.model.motor.B >= 0) {
                this.runOnce(`data.motor.B.direction = 1; data.motor.B.speed = ${this.model.motor.B}; return data;`);
            }
            else {
                this.runOnce(`data.motor.B.direction = 0; data.motor.B.speed = ${-this.model.motor.B}; return data;`);
            }
        },
        post(data) {
            let settings = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            };
            fetch("/", settings).then(res => res.text()).then(text => {
                console.log(text);
            });
        }
    },
    computed: {
        led0: {
            get() { return this.getModelLedColor(0); },
            set(newValue) { this.setModelLedColor(0, newValue); }
        },
        led1: {
            get() { return this.getModelLedColor(1); },
            set(newValue) { this.setModelLedColor(1, newValue); }
        },
        led2: {
            get() { return this.getModelLedColor(2); },
            set(newValue) { this.setModelLedColor(2, newValue); }
        },
        led3: {
            get() { return this.getModelLedColor(3); },
            set(newValue) { this.setModelLedColor(3, newValue); }
        },
        motorALeft() {
            if (this.motor.A.direction === 0) {
                let rate = (100 - this.motor.A.speed) / 2;
                return rate.toString() + "%";
            }
            else {
                return "50%"
            }
        },
        motorA() {
            let rate = this.motor.A.speed / 2;
            return rate.toString() + "%";
        },
        motorBLeft() {
            if (this.motor.B.direction === 0) {
                let rate = (100 - this.motor.B.speed) / 2;
                return rate.toString() + "%";
            }
            else {
                return "50%"
            }
        },
        motorB() {
            let rate = this.motor.B.speed / 2;
            return rate.toString() + "%";
        },
    },
    mounted() {
        async function getData() {
            let data = await fetch('/api/').then(res => res.json());
            return data;
        }

        setInterval(() => {
            getData().then(data => {
                this.led.brightness = data.led.brightness;
                this.led.leds = data.led.leds;
                this.irsensor.left = data.irsensor.left;
                this.irsensor.right = data.irsensor.right;
                this.irsensor.analog = data.irsensor.analog;
                this.motor.A.direction = data.motor.A.direction;
                this.motor.A.speed = data.motor.A.speed;
                this.motor.B.direction = data.motor.B.direction;
                this.motor.B.speed = data.motor.B.speed;

                if (window.userFunc) {
                    try {
                        let ret = window.userFunc(JSON.parse(JSON.stringify(data)));
                        if (ret) {
                            this.post(ret);
                        }
                    } catch (error) {
                        alert(error);
                        window.userFunc = null;
                    }
                }
            });
        }, 200)
    }
};
var app = Vue.createApp(App);
app.mount("#app");

window.userFunc = null;

window.editor = ace.edit("editor");
editor.setTheme("ace/theme/chrome");
editor.session.setMode("ace/mode/javascript");
editor.setValue("console.log(data);\nreturn data;\n");