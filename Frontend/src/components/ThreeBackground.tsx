import React, { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Points, PointMaterial } from "@react-three/drei";
import * as random from "maath/random";
import * as THREE from "three";

function StarField() {
    const ref = useRef<THREE.Group>(null!);

    const [sphere] = useMemo(() => {
        return [random.inSphere(new Float32Array(5001), { radius: 1.2 })];
    }, []);

    useFrame((state, delta) => {
        if (ref.current) {
            ref.current.rotation.x -= delta / 10;
            ref.current.rotation.y -= delta / 15;
        }
    });

    return (
        <group ref={ref}>
            <Points positions={sphere} stride={3} frustumCulled={false}>
                <PointMaterial
                    transparent
                    color="#ffa0e0"
                    size={0.005}
                    sizeAttenuation={true}
                    depthWrite={false}
                    blending={THREE.AdditiveBlending}
                />
            </Points>
        </group>
    );
}

export default function ThreeBackground() {
    return (
        // This component will be placed behind all other content
        <div className="absolute inset-0 -z-10">
            <Canvas camera={{ position: [0, 0, 1] }}>
                <color attach="background" args={['#000000']} />
                <StarField />
            </Canvas>
        </div>
    );
}