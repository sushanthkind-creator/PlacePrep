import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';
import { AXES, moveAngle, solutionFor } from './cubeMoves.js';

// A 3x3 Rubik's cube whose pose is a pure function of "solve progress" (0 → 1).
// The cube starts from a random scramble and plays the inverse moves in reverse,
// so scrolling forward solves it and scrolling back re-scrambles it exactly.

const AXIS_VECTORS = {
  x: new THREE.Vector3(1, 0, 0),
  y: new THREE.Vector3(0, 1, 0),
  z: new THREE.Vector3(0, 0, 1),
};

// Standard colour scheme: white top, green front, red right.
const STICKER_COLORS = {
  px: '#e6332a', // R – red
  nx: '#ff8a1f', // L – orange
  py: '#f4f4ef', // U – white
  ny: '#ffd31a', // D – yellow
  pz: '#19b35a', // F – green
  nz: '#1f63ff', // B – blue
};

const SPACING = 1.02;
const STICKER_SIZE = 0.8;
const STICKER_OFFSET = 0.502;

function easeInOutCubic(t) {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

function roundedSquareGeometry(size, radius) {
  const h = size / 2;
  const shape = new THREE.Shape();
  shape.moveTo(-h + radius, -h);
  shape.lineTo(h - radius, -h);
  shape.quadraticCurveTo(h, -h, h, -h + radius);
  shape.lineTo(h, h - radius);
  shape.quadraticCurveTo(h, h, h - radius, h);
  shape.lineTo(-h + radius, h);
  shape.quadraticCurveTo(-h, h, -h, h - radius);
  shape.lineTo(-h, -h + radius);
  shape.quadraticCurveTo(-h, -h, -h + radius, -h);
  return new THREE.ShapeGeometry(shape, 6);
}

export class RubiksCube {
  constructor(scramble) {
    this.group = new THREE.Group();
    this.solution = solutionFor(scramble);
    this.cubies = [];
    this.lastProgress = -1;

    this.bodyGeometry = new RoundedBoxGeometry(0.98, 0.98, 0.98, 4, 0.1);
    this.stickerGeometry = roundedSquareGeometry(STICKER_SIZE, 0.12);
    this.bodyMaterial = new THREE.MeshStandardMaterial({ color: '#121216', roughness: 0.42, metalness: 0.1 });
    this.stickerMaterials = Object.fromEntries(
      Object.entries(STICKER_COLORS).map(([face, color]) => [
        face,
        new THREE.MeshPhysicalMaterial({
          color,
          emissive: color,
          emissiveIntensity: 0,
          roughness: 0.38,
          clearcoat: 0.45,
          clearcoatRoughness: 0.3,
        }),
      ]),
    );

    this.buildCubies();
    this.snapshots = this.buildSnapshots(scramble);
  }

  buildCubies() {
    const faces = [
      { key: 'px', test: (p) => p.x === 1, rot: [0, Math.PI / 2, 0], off: [STICKER_OFFSET, 0, 0] },
      { key: 'nx', test: (p) => p.x === -1, rot: [0, -Math.PI / 2, 0], off: [-STICKER_OFFSET, 0, 0] },
      { key: 'py', test: (p) => p.y === 1, rot: [-Math.PI / 2, 0, 0], off: [0, STICKER_OFFSET, 0] },
      { key: 'ny', test: (p) => p.y === -1, rot: [Math.PI / 2, 0, 0], off: [0, -STICKER_OFFSET, 0] },
      { key: 'pz', test: (p) => p.z === 1, rot: [0, 0, 0], off: [0, 0, STICKER_OFFSET] },
      { key: 'nz', test: (p) => p.z === -1, rot: [0, Math.PI, 0], off: [0, 0, -STICKER_OFFSET] },
    ];

    for (let x = -1; x <= 1; x++) {
      for (let y = -1; y <= 1; y++) {
        for (let z = -1; z <= 1; z++) {
          const home = new THREE.Vector3(x, y, z);
          const cubie = new THREE.Group();
          cubie.add(new THREE.Mesh(this.bodyGeometry, this.bodyMaterial));
          for (const face of faces) {
            if (!face.test(home)) continue;
            const sticker = new THREE.Mesh(this.stickerGeometry, this.stickerMaterials[face.key]);
            sticker.rotation.set(...face.rot);
            sticker.position.set(...face.off);
            cubie.add(sticker);
          }
          this.group.add(cubie);
          this.cubies.push(cubie);
        }
      }
    }
  }

  // Integer positions + orientations of every cubie, before each solution move.
  buildSnapshots(scramble) {
    let state = {
      positions: this.cubies.map((_, i) => {
        const x = Math.floor(i / 9) - 1;
        const y = (Math.floor(i / 3) % 3) - 1;
        const z = (i % 3) - 1;
        return new THREE.Vector3(x, y, z);
      }),
      quaternions: this.cubies.map(() => new THREE.Quaternion()),
    };
    for (const move of scramble) state = applyMove(state, move);

    const snapshots = [state];
    for (const move of this.solution) {
      state = applyMove(state, move);
      snapshots.push(state);
    }
    return snapshots;
  }

  get moveCount() {
    return this.solution.length;
  }

  setProgress(progress) {
    const p = Math.min(1, Math.max(0, progress));
    if (p === this.lastProgress) return;
    this.lastProgress = p;

    const total = this.solution.length;
    const exact = p * total;
    const index = Math.min(total, Math.floor(exact));
    const state = this.snapshots[index];
    const move = index < total ? this.solution[index] : null;
    const turn = move ? easeInOutCubic(exact - index) : 0;
    const axisIndex = move ? AXES.indexOf(move.axis) : -1;
    const q = move && turn > 0
      ? new THREE.Quaternion().setFromAxisAngle(AXIS_VECTORS[move.axis], moveAngle(move) * turn)
      : null;

    this.cubies.forEach((cubie, i) => {
      const pos = state.positions[i];
      const quat = state.quaternions[i];
      if (q && pos.getComponent(axisIndex) === move.layer) {
        cubie.position.copy(pos).applyQuaternion(q).multiplyScalar(SPACING);
        cubie.quaternion.copy(q).multiply(quat);
      } else {
        cubie.position.copy(pos).multiplyScalar(SPACING);
        cubie.quaternion.copy(quat);
      }
    });
  }

  dispose() {
    this.bodyGeometry.dispose();
    this.stickerGeometry.dispose();
    this.bodyMaterial.dispose();
    Object.values(this.stickerMaterials).forEach((m) => m.dispose());
  }
}

function applyMove(state, move) {
  const axisIndex = AXES.indexOf(move.axis);
  const q = new THREE.Quaternion().setFromAxisAngle(AXIS_VECTORS[move.axis], moveAngle(move));
  const positions = [];
  const quaternions = [];
  state.positions.forEach((pos, i) => {
    if (pos.getComponent(axisIndex) === move.layer) {
      const p = pos.clone().applyQuaternion(q);
      positions.push(new THREE.Vector3(Math.round(p.x), Math.round(p.y), Math.round(p.z)));
      quaternions.push(q.clone().multiply(state.quaternions[i]).normalize());
    } else {
      positions.push(pos.clone());
      quaternions.push(state.quaternions[i].clone());
    }
  });
  return { positions, quaternions };
}
