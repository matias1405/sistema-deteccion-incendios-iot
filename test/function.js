const x_size = 26;
const y_size = 18;

const p_inicial = [5, 7]; // x, y
const p_final = [8, 11];

const temp = msg.payload;

var ls = flow.get("heatmap");

for (let y = 0; y < y_size; y++) {
    if ((p_inicial[1] - 1) <= y && (p_final[1] - 1) >= y) {
        for (let x = 0; x < x_size; x++) {
            if ((p_inicial[0] - 1) <= x && (p_final[0] - 1) >= x) {
                ls[y_size * x + y] = temp;
            }
        }
    }
}
msg.payload = ls;
return msg;