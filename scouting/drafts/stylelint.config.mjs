export default {
  plugins: ['stylelint-declaration-strict-value'],
  rules: {
    'scale-unlimited/declaration-strict-value': [['/color$/', 'background-color', 'border-color', 'fill', 'stroke'], { ignoreValues: ['transparent','inherit','currentColor','none','initial','unset'], disableFix: true, severity: 'warning' }],
    'color-no-invalid-hex': true,
    'declaration-property-value-disallowed-list': [{ 'outline': ['none','0'], 'transition': ['/all/'] }, { message: 'avoid outline:none / transition:all' }],
    'declaration-no-important': true,
    'font-family-no-missing-generic-family-keyword': true,
    'unit-disallowed-list': [['vh'], { ignoreProperties: {} , severity:'warning' }],
  }
};
