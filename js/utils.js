/**
 * @param {number} radius
 * @param {number} phi
 * @param {number} theta
 */
function computeX(radius, phi, theta) {
    return radius * Math.sin(theta) * Math.cos(phi);
}

/**
 * @param {number} radius
 * @param {number} phi
 * @param {number} theta
 */
function computeY(radius, phi, theta) {
    return radius * Math.sin(theta) * Math.sin(phi);
}

/**
 * @param {number} radius
 * @param {number} theta
 */
function computeZ(radius, theta) {
    return radius * Math.cos(theta);
}