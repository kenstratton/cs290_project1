// MODE変数でmodeの値を設定する(development or production)
const MODE = "development";
// MODE変数がproductionならisProductionをtrueにする
const isProduction = MODE === "production";

let array = [ "JavaScript", 0, 1, " ", "", undefined, null, isProduction && {test: /\.(gif|png|jpg|svg)$/}, false];

let new_array = array.filter(Boolean);

console.log(new_array);

class Test {
  constructor(name) {
    this.name = name;
  }

  logger () {
    console.log("Hello", this.name);
  }
}
let test = new Test('world');
test.logger();