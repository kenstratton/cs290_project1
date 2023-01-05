// node.jsの標準モジュールpathの読み込み
const path  = require('path');
// MODE変数でmodeの値を設定する。
const MODE = "development";
// MODE変数がdevelopmentならsourceMapStatusをtrueにする。
const sourceMapStatus = MODE === "development";
// バンドルしたJavaScriptからスタイルシートの箇所をcssファイルとして出力するplugin
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const cssInline = false;
if(cssInline) {
  styleLoader = 'style-loader';
} else {
  styleLoader = { loader: MiniCssExtractPlugin.loader };
}


// moduleオブジェクトのexportsプロパティに値(オブジェクト: プロパティ)を設定
module.exports = {
  // __dirname = Node.js標準のグローバル変数、絶対パスでディレクトリ名まで
  context: path.join(__dirname, "/src"),

  // webpackがビルドを始める際の開始点(default = ./src/index.js)
  // 複数をまとめてバンドルする場合 [ "./index.js", "./sub.js" ... ]
  // -> (output) filename: "[name].bundle.js" [name]はエントリーポイント名がくる
  // 複数をそれぞれバンドルする場合 { main: "./sub.js", sub: "./sub.js"}
  // -> (output) filename: "bundle.js"
  entry: './js/index.js',

  // webpackコマンドをmodeオプションなしで実行(--mode development)
  // バンドル対象が完了したらproductionで実行
  mode: MODE,

  // ソースマップを出力(--devtool=source-map)
  devtool: "hidden-source-map",

  // ビルドしたファイルをどこ/どんな名前で出力するかを指定
  output: {
    //  出力ファイルのディレクト名
    path: `${__dirname}/dist`,
    // 出力ファイル名 + 出力先の設定
    filename: "./assets/js/main.js",
    // 出力ファルダ内のファイルを全て削除してから出力
    clean: {
      keep: /index.html/ //index.html をキープ（削除しない）
    }
  },

  // watch: (ファイル変更を監視し、自動でリビルド: 再構築)
  watch: false,
  watchOptions: {
    // ignored: 文字列または正規表現で監査対象外を指定(ワイルドカード可)
    ignored: ['foo/**/*.js', 'node_modules/**']
  },

  // 最適化(圧縮)
  optimization: {
    // minimize: 出力ファイルの圧縮(dflt = dev: false, prod: true)
    minimize: true
  },

  // ローダーなどのモジュールの設定
  module: {
    // 配列の各要素に各ローダーのルールを設定
    rules: [
      {
        // test: 正規表現などで対象ファイルを指定
        // test: /\.(scss|css)$/,
        // test: /\.css$/,
        test: /\.scss$/,

        // use: 使用するローダーを指定
        use: [
          // ? CSSファイルを書き出すオプションを有効にする
          // MiniCssExtractPlugin.loader,
          // {
          //   loader: MiniCssExtractPlugin.loader
          // },

          // style-loader - バンドルされたCSSをHTMLでスタイルシートとして読み込む
          // 'style-loader',

          styleLoader,

          // css-loader - cssをjsにバンドル
          {
            loader: 'css-loader',
            options: {
              // CSS内の画像等のurlの有効無効を設定(dflt = true)
              url: false,
              sourceMap: sourceMapStatus,

              // 0 => no loaders (default);
              // 1 => postcss-loader;
              // 2 => postcss-loader, sass-loader
              importLoaders: 2
            }
          },

          // ? PostCSSのための設定
          {
            loader: "postcss-loader",
            options: {
              // PostCSS側でもソースマップを有効にする
              // sourceMap: true,
              postcssOptions: {
                plugins: [
                  // Autoprefixerを有効化
                  // ベンダープレフィックスを自動付与する
                  // require('autoprefixer')({ grid: true })
                  [ 'autoprefixer', { grid: true } ],

                ],
              },
            },
          },

          // sass-loader - SassをCSSに変換かつjsにバンドル
          {
            loader: 'sass-loader',
            options: {
              sourceMap: sourceMapStatus
            }
          }
        ]
      },

      // css内の画像をバンドル - 画像をbase64というjsで使用可能なデータ形式に変換
      {
        test: /\.(gif|png|jpg|svg)$/,
        // type: 画像をBase64にエンコードして埋め込み
        // asset/inline - 一括で全てのファイルをバンドル
        // asset/resource - バンドルせずに画像を出力
        // asset - どっちつかずの設定, のちのparserプロパティでエンコードした場合の容量を加味してバンドルの有無を設定
        type: "asset",
        // parser.dataUrlCondition.maxSize: バンドルする最大ファイル値を設定 下記では100KB
        parser: {
          dataUrlCondition: {
            maxSize: 100 * 1024
          }
        }
      }
    ]
  },

  plugins: [
    // バンドルしたjsからスタイルシート箇所を別cssファイルとして出力(早い段階で適用させるため等)
    new MiniCssExtractPlugin({
      // 出力先の設定
      filename: "assets/css/main.css"
    })
  ]

};