module.exports = {
  require: [
    'features/step-definitions/**/*.js',
    'features/step-definitions/*.js'
  ],
  paths: ['features/**/*.feature'],
  format: [
    'progress-bar',
    'json:cucumber-report.json',
    'html:cucumber-report.html'
  ],
  formatOptions: {
    colorsEnabled: true,
    snippetInterface: 'async-await'
  },
  publishQuiet: true
};