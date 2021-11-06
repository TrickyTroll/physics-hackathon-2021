/**
 * @param {number} radius
 * @param {number} phi
 * @param {number} theta
 */
function computeX(radius, phi, theta) {
    return radius * Math.sin(phi) * Math.cos(theta);
}

/**
 * @param {number} radius
 * @param {number} phi
 * @param {number} theta
 */
function computeY(radius, phi, theta) {
    return radius * Math.sin(phi) * Math.sin(theta);
}

/**
 * @param {number} radius
 * @param {number} phi
 */
function computeZ(radius, phi) {
    return radius * Math.cos(phi);
}