export function useCurrencyFormatter(currency = 'USD', locale = 'en-US') {
  const format = (value) =>
    new Intl.NumberFormat(locale, { style: 'currency', currency }).format(value)
  return { format }
}
