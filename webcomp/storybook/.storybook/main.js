// eslint-disable-next-line @typescript-eslint/no-var-requires
const webpack = require("webpack");
const path = require("path");

module.exports = {
  webpackFinal: async config => {
    const babelLoaderRule = config.module.rules.find(
      (rule) => rule.test.toString() === /\.(mjs|tsx?|jsx?)$/.toString()
    );
    babelLoaderRule.include = [path.resolve(__dirname, "../..")];

    const svgRule = config.module.rules.find(rule =>
      "test.svg".match(rule.test)
    );
    svgRule.exclude = /\.svg$/;

    config.module.rules.push({
      test: /\.svg$/,
      use: "raw-loader",
      include: [path.resolve(__dirname, "../..")]
    });

    return config;
  },
  stories: ["../stories/**/*.stories.mdx", "../stories/**/*.stories.@(js|jsx|ts|tsx)"],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
    {
      name: "storybook-addon-sass-postcss",
      options: {
        rule: {
          test: /\.(scss|sass)$/i,
        },
        cssLoaderOptions: {
          modules: true,
        },
      },
    },
  ],
  framework: "@storybook/react",
};
