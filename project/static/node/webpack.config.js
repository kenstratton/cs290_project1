//* モジュール
// path(node.jsの標準モジュール)の読み込み
const path  = require('path');


//* Webpackプラグイン
// バンドルしたJavaScriptからスタイルシートの箇所をcssファイルとして出力する
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
// 指定ファイルをコピーして出力(出力元と先を合わせる)
//! const CopyPlugin = require('copy-webpack-plugin');
// 画像を圧縮する
const ImageminPlugin = require('imagemin-webpack-plugin').default;
// jpeg形式ファイルの圧縮に対応する
const ImageminMozjpeg = require('imagemin-mozjpeg');


//* moduleオブジェクトのexportsプロパティに値(オブジェクト: プロパティ)を設定
module.exports = (env, argv) => {
  // MODE変数でmodeの値を設定する(development or production)
  const MODE = argv.mode;
  // MODE変数がproductionならisProductionをtrueにする
  const isProduction = MODE === "production";

  // MODE変数がdevelopmentの場合
  // -> sourceMap: 設定する
  // -> css出力:    style-loader (インライン形式)
  // -> css最適化:  設定しない
  // MODE変数がproductionの場合
  // -> sourceMap: 設定しない
  // -> css出力:    MiniCssExtractPlugin.loader (別cssファイル形式)
  // -> css最適化:  設定する
  if (MODE === "development") {
    sourceMap = "source-map";
    styleLoader = 'style-loader';
    cssMinifier = null;
  } 
  else if (MODE === "production") {
    sourceMap = false;
    styleLoader = { loader: MiniCssExtractPlugin.loader };
    cssMinifier = [ 'cssnano', { preset: 'default' } ];
  }

  // ビルドの設定情報を返す
  return {
    // __dirname = Node.js標準のグローバル変数、絶対パスでディレクトリ名まで
    context: path.join(__dirname, "/src"),

    // webpackがビルドを始める際の開始点(default = ./src/index.js)
    // 複数をまとめてバンドルする場合 [ "./index.js", "./sub.js" ... ]
    // -> (output) filename: "bundle.js"
    // 複数をそれぞれバンドルする場合 { main: "./sub.js", sub: "./sub.js"}
    // -> (output) filename: "[name].bundle.js" [name]はエントリーポイント名がくる
    entry: './js/index.js',

    // ソースマップを出力(--devtool=source-map)
    devtool: sourceMap,

    // ビルドしたファイルをどこ/どんな名前で出力するかを指定
    output: {
      // 出力ファイルのディレクト名
      path: `${__dirname}/dist`,
      // 出力ファイル名 + 出力先の設定
      filename: (isProduction && "./js/main.min.js") || (isProduction || "./js/main.js"),
      // assetファイルの出力先設定
      assetModuleFilename: "img/[name][ext]'",
      // 出力ファルダ内のファイルを全て削除してから出力({keep: 保護ファイル})
      clean: true
    },

    // トランスパイルの対象となるファイルの拡張子を指定
    resolve: {
      extensions: ['*', '.webpack.js', '.js']
    },

    // watch: ファイル変更を監視し、自動でリビルド
    // watchOptions: watch実行時のオプション
    // > ignored: 文字列または正規表現で監査対象外を指定(ワイルドカード可))
    watchOptions: {
      ignored: ['node_modules/**']
    },

    // 最適化(圧縮)
    optimization: {
      // minimize: 出力ファイルの圧縮(dflt = dev: false, prod: true)
      minimize: isProduction
    },

    // ローダーなどのモジュールを設定
    module: {
      // 配列の各要素に各ローダーのルールを設定
      rules: [
        // JSのトランスパイル(レガシーブラウザ対応のため)
        {
          // test: 正規表現で対象ファイルを指定
          test: /\.js$/,
          // exclude: 正規表現でloaderの対象外とするディレクトリ等を指定
          exclude: /node_modules/,
          // use: 使用するローダーを指定
          use: {
            loader: 'babel-loader',
            options: {
              presets: [ '@babel/preset-env' ]
            }
          }
        },

        // CSS関連
        {
          // test: /\.(css|scss)$/,
          test: /\.(c|sc)ss$/,
          use: [
            // CSSファイルを書き出すオプションを有効化
            // バンドルされたCSSをHTMLでスタイルシートとして読み込む
            styleLoader,

            // css-loader - cssをjsにバンドル
            {
              loader: 'css-loader',
              options: {
                url: true, // CSS内画像等のurl利用の可否を設定(dflt = true)
                // 0 => no loaders (default);
                // 1 => postcss-loader;
                // 2 => postcss-loader, sass-loader
                importLoaders: 2
              }
            },

            // PostCSSのための設定
            {
              loader: "postcss-loader",
              options: {
                postcssOptions: {
                  plugins: [
                    // 最新のCSSを古いブラウザでも対応できるように変換
                    [
                      "postcss-preset-env",
                      {
                        // サポートするブラウザを指定
                        browsers: "last 2 versions, > 0.5%, not dead",
                        // ポリフィルする CSS 機能を決定(stage 0 through 4)
                        // stage: 3,
                        // 特定のCSS機能を有効
                        // features: {"nesting-rules": 3},
                        // ベンダープレフィックスを自動付与
                        autoprefixer: { grid: true },
                      },
                    ],
                    // CSSプロパティをソート
                    [
                      'css-declaration-sorter', 
                      { 
                        order: 'alphabetical' 
                      }
                    ],
                    // CSSのminifyを行う
                    cssMinifier
                  ],
                },
              },
            },

            // sass-loader - SassをCSSに変換かつjsにバンドル
            { loader: 'sass-loader' }
          ]
        },

        // css内の画像をバンドル - 画像をbase64というjs用のデータ形式に変換し埋め込む
        {
          test: /\.(gif|png|jpg|svg)$/,
          // asset/inline - 一括で全てのファイルをバンドル
          // asset/resource - バンドルせずに画像を出力
          // asset - どっちつかず, parserプロパティでエンコードした場合の容量を加味しバンドル有無を設定
          type: "asset",
          // parser.dataUrlCondition.maxSize: バンドルする最大ファイル値を設定 下記では100KB
          parser: {
            dataUrlCondition: {
              maxSize: 100 * 1024
            }
          }
        },

        // Bootstrap内のインラインSVGファイルを抽出
        // SVGを別で展開しCSSから適切に参照させる(data url schemeをブロックするコンテンツがある場合の対処)
        {
          mimetype: 'image/svg+xml', // MIMEタイプ - ファイルの種類
          scheme: 'data', // data url scheme - インラインにデータを埋めこむ手段を提供するURIスキーム
          type: 'asset/resource',
          generator: {
            filename: 'icons/[hash].svg'
          }
        },
      ]
    },

    // プラグイン
    plugins: [
      // バンドルしたjsからスタイルシート箇所を別cssファイルとして出力(早い段階で適用させるため)
      new MiniCssExtractPlugin({
        // 出力先の設定
        filename: "css/main.min.css"
      }),

      
      //! (必要性審議) 対象がcss内画像のみのためasset moduleで事足りる。今後、対象ファイルの追加があれば使用。
      // 指定ファイルをコピーして出力(出力元と先を合わせる)... 
      // new CopyPlugin({
      //   patterns: [
      //     {
      //       from: `${__dirname}/src/img`,
      //       to: `${__dirname}/dist/img/[name]_min[ext]`
      //     }
      //   ]
      // }),

      // 各ファイル形式に合わせて画像を圧縮
      new ImageminPlugin({
        test: /\.(jpe?g|png|gif|svg)$/i,
        pngquant: {
          quality: '70-85'
        },
        gifsicle: {
          interlaced: false,
          optimizationLevel: 9,
          colors: 256
        },
        plugins: [
          ImageminMozjpeg({
            quality: 85,
            progressive: true
          })
        ],
        svgo: {},
      })
    ]

  }

};