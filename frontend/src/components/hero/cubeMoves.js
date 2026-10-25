// Pure Rubik's cube move logic, kept free of three.js so the page can use it
// without pulling the 3D bundle into the main chunk.

export const AXES = ['x', 'y', 'z'];
// Face letters indexed by [axis][layer === 1 ? 1 : 0]
const FACE_LETTERS = { x: ['L', 'R'], y: ['D', 'U'], z: ['B', 'F'] };

export function generateScramble(count = 18, rng = Math.random) {
  const moves = [];
  let lastAxis = null;
  while (moves.length < count) {
    const axis = AXES[Math.floor(rng() * 3)];
    if (axis === lastAxis) continue; // avoids moves that cancel or merge
    moves.push({ axis, layer: rng() < 0.5 ? -1 : 1, dir: rng() < 0.5 ? 1 : -1 });
    lastAxis = axis;
  }
  return moves;
}

export function invertMove(move) {
  return { ...move, dir: -move.dir };
}

// Moves that undo the scramble, in the order they are played.
export function solutionFor(scramble) {
  return scramble.slice().reverse().map(invertMove);
}

export function moveNotation({ axis, layer, dir }) {
  return FACE_LETTERS[axis][layer === 1 ? 1 : 0] + (dir === -1 ? "'" : '');
}

// Clockwise (as seen looking at the face) is a negative rotation about the face's outward normal.
export function moveAngle({ layer, dir }) {
  return -layer * dir * (Math.PI / 2);
}
