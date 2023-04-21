// eslint-disable-next-line @typescript-eslint/no-var-requires
const webpack = require("webpack");
const path = require("path");

module.exports = {
  webpackFinal: async config => {

    // Storybook detect the document root by using .git,
    // but we don't have .git inside a docker image.
    // Apply the following workaround:
    // https://darekkay.com/blog/storybook-separate-folder/
    const babelLoaderRule = config.module.rules.find(
      (rule) => rule.test.toString() === /\.(mjs|tsx?|jsx?)$/.toString()
    );
    babelLoaderRule.include = [path.resolve(__dirname, "../..")];

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
