export function hasRange(text, min, max) {
  return text.length >= min && text.length <= max
}

export function hasUppercaseLetter(text) {
  return /[A-Z]/.test(text)
}

export function hasLowercaseLetter(text) {
  return /[a-z]/.test(text)
}

export function hasDigit(text) {
  return /\d/.test(text)
}

export function hasSpecialCharacter(text) {
  return /[^A-Za-z0-9]/.test(text)
}
