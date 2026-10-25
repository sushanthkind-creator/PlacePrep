import * as THREE from 'three';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import { animate } from 'animejs';
import 'animejs/adapters/three';
import { RubiksCube } from './RubiksCube.js';

const X_AXIS = new THREE.Vector3(1, 0, 0);
const Y_AXIS = new THREE.Vector3(0, 1, 0);
const DRAG_SPEED = 0.008;
const KEY_STEP = 0.18;
const IDLE_SPIN_DELAY = 2500;
// Rough on-screen footprint of the cube in any orientation, used to fit narrow screens.
const CUBE_FOOTPRINT = 5.4;

function easeInOutCubic(t) {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

function makeShadowTexture() {
  const size = 256;
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext('2d');
  const gradient = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
  gradient.addColorStop(0, 'rgba(0,0,0,0.85)');
  gradient.addColorStop(0.55, 'rgba(0,0,0,0.25)');
  gradient.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, size, size);
  return new THREE.CanvasTexture(canvas);
}

/**
 * Mounts the interactive cube into `container`.
 * `getState()` is polled every frame and returns { solve, reveal } in 0..1.
 * Throws if WebGL is unavailable so the caller can show a fallback.
 */
export function createCubeStage(container, { scramble, getState, reducedMotion }) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
  const coarsePointer = window.matchMedia('(pointer: coarse)').matches;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, coarsePointer ? 1.5 : 2));
  // Neutral tone mapping keeps the sticker colours saturated (ACES washes them out).
  renderer.toneMapping = THREE.NeutralToneMapping;
  renderer.toneMappingExposure = 0.95;

  const canvas = renderer.domElement;
  canvas.className = 'cube-canvas';
  canvas.tabIndex = 0;
  canvas.setAttribute('role', 'img');
  canvas.setAttribute('aria-label', "3D Rubik's cube. Drag it, or focus it and use the arrow keys, to rotate.");
  container.appendChild(canvas);

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  const envTexture = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environment = envTexture;
  scene.environmentIntensity = 0.65;

  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);
  camera.position.set(0, 0, 13);

  const keyLight = new THREE.DirectionalLight('#ffffff', 1.1);
  keyLight.position.set(4, 6, 8);
  const rimLight = new THREE.DirectionalLight('#8f7bff', 0.9);
  rimLight.position.set(-6, -2, -6);
  scene.add(keyLight, rimLight);

  // Nested groups so each motion owns one transform:
  // layout (slides aside for the login card) → float (idle bob) → celebrate (spin when solved) → drag (user) → cube
  const layoutGroup = new THREE.Group();
  const floatGroup = new THREE.Group();
  const celebrateGroup = new THREE.Group();
  const dragGroup = new THREE.Group();
  const cube = new RubiksCube(scramble);
  dragGroup.add(cube.group);
  celebrateGroup.add(dragGroup);
  floatGroup.add(celebrateGroup);
  layoutGroup.add(floatGroup);
  scene.add(layoutGroup);
  dragGroup.quaternion.setFromEuler(new THREE.Euler(0.45, -0.65, 0));

  const shadowTexture = makeShadowTexture();
  const shadowGeometry = new THREE.PlaneGeometry(6, 6);
  const shadowMaterial = new THREE.MeshBasicMaterial({ map: shadowTexture, transparent: true, depthWrite: false, opacity: 0.5 });
  const shadow = new THREE.Mesh(shadowGeometry, shadowMaterial);
  shadow.rotation.x = -Math.PI / 2;
  shadow.position.y = -3.2;
  layoutGroup.add(shadow);

  // ---- Rotation input -------------------------------------------------------
  const drag = { active: false, pointerId: null, x: 0, y: 0, vx: 0, vy: 0, lastInput: -Infinity };
  const qTmp = new THREE.Quaternion();

  function rotateBy(ax, ay) {
    qTmp.setFromAxisAngle(Y_AXIS, ax);
    dragGroup.quaternion.premultiply(qTmp);
    qTmp.setFromAxisAngle(X_AXIS, ay);
    dragGroup.quaternion.premultiply(qTmp);
  }

  function onPointerDown(e) {
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    drag.active = true;
    drag.pointerId = e.pointerId;
    drag.x = e.clientX;
    drag.y = e.clientY;
    drag.vx = drag.vy = 0;
    drag.lastInput = performance.now();
    canvas.setPointerCapture(e.pointerId);
    canvas.classList.add('is-grabbing');
  }

  function onPointerMove(e) {
    if (!drag.active || e.pointerId !== drag.pointerId) return;
    const dx = e.clientX - drag.x;
    const dy = e.clientY - drag.y;
    drag.x = e.clientX;
    drag.y = e.clientY;
    // On touch, vertical swipes scroll the page (touch-action: pan-y), so only spin horizontally.
    const ax = dx * DRAG_SPEED;
    const ay = e.pointerType === 'touch' ? 0 : dy * DRAG_SPEED;
    rotateBy(ax, ay);
    drag.vx = ax;
    drag.vy = ay;
    drag.lastInput = performance.now();
  }

  function onPointerUp(e) {
    if (e.pointerId !== drag.pointerId) return;
    drag.active = false;
    drag.pointerId = null;
    canvas.classList.remove('is-grabbing');
    if (canvas.hasPointerCapture(e.pointerId)) canvas.releasePointerCapture(e.pointerId);
  }

  function onKeyDown(e) {
    const steps = { ArrowLeft: [-KEY_STEP, 0], ArrowRight: [KEY_STEP, 0], ArrowUp: [0, -KEY_STEP], ArrowDown: [0, KEY_STEP] };
    const step = steps[e.key];
    if (!step) return;
    e.preventDefault();
    rotateBy(step[0], step[1]);
    drag.vx = drag.vy = 0;
    drag.lastInput = performance.now();
  }

  canvas.addEventListener('pointerdown', onPointerDown);
  canvas.addEventListener('pointermove', onPointerMove);
  canvas.addEventListener('pointerup', onPointerUp);
  canvas.addEventListener('pointercancel', onPointerUp);
  canvas.addEventListener('keydown', onKeyDown);

  // ---- Layout ---------------------------------------------------------------
  const view = { width: 1, height: 1, aspect: 1, fitScale: 1 };

  function resize() {
    const width = Math.max(1, container.clientWidth);
    const height = Math.max(1, container.clientHeight);
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    view.height = 2 * camera.position.z * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
    view.width = view.height * camera.aspect;
    view.aspect = camera.aspect;
    view.fitScale = Math.min(1, (view.width * 0.92) / CUBE_FOOTPRINT);
  }

  function applyLayout(reveal) {
    const e = easeInOutCubic(reveal);
    if (view.aspect >= 1) {
      layoutGroup.position.set(-view.width * 0.2 * e, 0, 0);
      layoutGroup.scale.setScalar(view.fitScale * (1 - 0.12 * e));
    } else {
      layoutGroup.position.set(0, view.height * 0.27 * e, 0);
      layoutGroup.scale.setScalar(view.fitScale * (1 - 0.42 * e));
    }
  }

  const resizeObserver = new ResizeObserver(resize);
  resizeObserver.observe(container);
  resize();

  // ---- Celebration (anime.js three adapter animates Object3D + materials) ----
  const stickerMaterials = Object.values(cube.stickerMaterials);
  let celebrations = [];

  function celebrate() {
    if (reducedMotion) return;
    celebrations.forEach((a) => a.pause());
    celebrations = [
      animate(celebrateGroup, {
        rotateY: [0, 360],
        duration: 1600,
        ease: 'inOutQuart',
      }),
      animate(celebrateGroup, {
        scale: [
          { to: 1.1, duration: 380, ease: 'outQuad' },
          { to: 1, duration: 1100, ease: 'outElastic(1, .5)' },
        ],
      }),
      animate(stickerMaterials, {
        emissiveIntensity: [
          { to: 0.55, duration: 320, ease: 'outQuad' },
          { to: 0, duration: 1100, ease: 'inOutSine' },
        ],
      }),
    ];
  }

  // ---- Render loop ----------------------------------------------------------
  let rafId = 0;
  let running = false;
  let lastTime = performance.now();
  let elapsed = 0;
  let celebrated = false;

  function frame(now) {
    rafId = requestAnimationFrame(frame);
    const dt = Math.min(0.05, (now - lastTime) / 1000);
    lastTime = now;
    elapsed += dt;

    const { solve, reveal } = getState();
    cube.setProgress(solve);

    if (solve >= 1 && !celebrated) {
      celebrated = true;
      celebrate();
    } else if (solve < 0.9 && celebrated) {
      celebrated = false;
    }

    if (!drag.active) {
      if (Math.abs(drag.vx) + Math.abs(drag.vy) > 1e-4) {
        rotateBy(drag.vx, drag.vy);
        drag.vx *= 0.93;
        drag.vy *= 0.93;
      } else if (!reducedMotion && now - drag.lastInput > IDLE_SPIN_DELAY) {
        rotateBy(0.12 * dt, 0);
      }
    }

    if (!reducedMotion) {
      floatGroup.position.y = Math.sin(elapsed * 1.3) * 0.14;
      floatGroup.rotation.z = Math.sin(elapsed * 0.9) * 0.03;
      const lift = (floatGroup.position.y + 0.14) / 0.28;
      shadow.scale.setScalar(1 - lift * 0.12);
      shadowMaterial.opacity = 0.5 - lift * 0.15;
    }

    applyLayout(reveal);
    renderer.render(scene, camera);
  }

  function start() {
    if (running) return;
    running = true;
    lastTime = performance.now();
    rafId = requestAnimationFrame(frame);
  }

  function stop() {
    running = false;
    cancelAnimationFrame(rafId);
  }

  // Only render while the stage is on screen.
  const visibilityObserver = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) start();
    else stop();
  });
  visibilityObserver.observe(container);

  return {
    dispose() {
      stop();
      celebrations.forEach((a) => a.pause());
      visibilityObserver.disconnect();
      resizeObserver.disconnect();
      canvas.removeEventListener('pointerdown', onPointerDown);
      canvas.removeEventListener('pointermove', onPointerMove);
      canvas.removeEventListener('pointerup', onPointerUp);
      canvas.removeEventListener('pointercancel', onPointerUp);
      canvas.removeEventListener('keydown', onKeyDown);
      cube.dispose();
      shadowGeometry.dispose();
      shadowMaterial.dispose();
      shadowTexture.dispose();
      envTexture.dispose();
      pmrem.dispose();
      renderer.dispose();
      canvas.remove();
    },
  };
}
