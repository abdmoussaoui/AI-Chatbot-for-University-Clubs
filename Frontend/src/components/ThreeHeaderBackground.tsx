import React, { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import * as THREE from "three";

// Component for the flowing wave plane
const Waves = () => {
  const meshRef = useRef<THREE.Mesh>(null!);
  const geometryRef = useRef<THREE.PlaneGeometry>(null!);

  useFrame(({ clock }) => {
    if (!geometryRef.current) return;

    const time = clock.getElapsedTime();
    const positions = geometryRef.current.attributes.position
      .array as Float32Array;

    for (let i = 0; i < positions.length; i += 3) {
      const x = positions[i];
      const y = positions[i + 1];
      // Animate z-position of each vertex
      positions[i + 2] =
        Math.sin(x * 0.5 + time) * 0.3 + Math.cos(y * 0.5 + time) * 0.3;
    }

    geometryRef.current.attributes.position.needsUpdate = true;
  });

  return (
    <mesh ref={meshRef} rotation-x={-Math.PI / 4} position-z={-2}>
      <planeGeometry ref={geometryRef} args={[20, 20, 50, 50]} />
      <meshBasicMaterial
        color={0x1976d2}
        transparent
        opacity={0.15}
        wireframe
      />
    </mesh>
  );
};

// Component for the background particles
const Particles = ({ count = 150 }) => {
  const pointsRef = useRef<THREE.Points>(null!);

  const positions = useMemo(() => {
    const posArray = new Float32Array(count * 3);
    for (let i = 0; i < count * 3; i++) {
      posArray[i] = (Math.random() - 0.5) * 10;
    }
    return posArray;
  }, [count]);

  useFrame(({ clock }) => {
    if (pointsRef.current) {
      pointsRef.current.rotation.y = clock.getElapsedTime() * 0.2;
      pointsRef.current.rotation.x = clock.getElapsedTime() * 0.1;
    }
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={positions.length / 3}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.025}
        color={0x64b5f6}
        transparent
        opacity={0.8}
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
};

// Component for the floating geometric shapes
const Shapes = ({ count = 8 }) => {
  const groupRef = useRef<THREE.Group>(null!);

  const shapes = useMemo(() => {
    return Array.from({ length: count }, () => ({
      position: new THREE.Vector3(
        (Math.random() - 0.5) * 8,
        (Math.random() - 0.5) * 6,
        (Math.random() - 0.5) * 4
      ),
      rotation: new THREE.Euler(
        Math.random() * Math.PI,
        Math.random() * Math.PI,
        Math.random() * Math.PI
      ),
      isBox: Math.random() > 0.5,
      color: new THREE.Color().setHSL(0.6 + Math.random() * 0.2, 0.7, 0.6),
      speedFactor: 0.1 + Math.random() * 0.2,
    }));
  }, [count]);

  useFrame(({ clock }) => {
    if (groupRef.current) {
      groupRef.current.children.forEach((shape, index) => {
        const speed = shapes[index].speedFactor;
        shape.rotation.x += 0.01 * speed;
        shape.rotation.y += 0.01 * speed;
        shape.position.y +=
          Math.sin(clock.getElapsedTime() * speed + index) * 0.01;
      });
    }
  });

  return (
    <group ref={groupRef}>
      {shapes.map((props, i) => (
        <mesh key={i} position={props.position} rotation={props.rotation}>
          {props.isBox ? (
            <boxGeometry args={[0.2, 0.2, 0.2]} />
          ) : (
            <sphereGeometry args={[0.1, 16, 16]} />
          )}
          <meshBasicMaterial color={props.color} transparent opacity={0.7} />
        </mesh>
      ))}
    </group>
  );
};

const ThreeHeaderBackground: React.FC = () => {
  return (
    <div className="absolute inset-0 w-full h-full" style={{ zIndex: 0 }}>
      <Canvas
        camera={{ position: [0, 0, 5], fov: 75 }}
        gl={{ antialias: true, alpha: true }}
      >
        <ambientLight intensity={0.5} />
        <Particles />
        <Waves />
        <Shapes />
      </Canvas>
    </div>
  );
};

export default ThreeHeaderBackground;