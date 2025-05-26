import { useEffect, useRef } from 'react';
import * as THREE from 'three';

const ThreeBackground = () => {
  const mountRef = useRef(null);

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return;

    // Scene setup with dark background
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0612); // Deep purple-black
    
    const camera = new THREE.PerspectiveCamera(
      75, 
      mount.clientWidth / mount.clientHeight, 
      0.1, 
      1000
    );
    const renderer = new THREE.WebGLRenderer({ 
      alpha: false,
      antialias: true,
      powerPreference: "high-performance"
    });
    
    renderer.setSize(mount.clientWidth, mount.clientHeight);
    mount.appendChild(renderer.domElement);

    // Create particles with varied colors
    const createParticles = () => {
      const particleCount = 1000; // Increased for better effect
      const particlesGeometry = new THREE.BufferGeometry();
      
      const posArray = new Float32Array(particleCount * 3);
      const colorArray = new Float32Array(particleCount * 3);
      
      // Color palette - array of RGB values in neopurple range
      const colorPalette = [
        [0.4, 0.0, 0.6],   // Deep purple
        [0.6, 0.0, 0.8],   // Bright purple
        [0.3, 0.0, 0.5],   // Dark purple
        [0.5, 0.2, 0.7],   // Lavender
        [0.7, 0.0, 0.9],   // Neon purple
        [0.8, 0.4, 1.0],   // Light purple
        [0.2, 0.0, 0.4]    // Very dark purple
      ];

      for(let i = 0; i < particleCount * 3; i += 3) {
        // Random positions in a larger volume
        posArray[i] = (Math.random() - 0.5) * 15;
        posArray[i+1] = (Math.random() - 0.5) * 15;
        posArray[i+2] = (Math.random() - 0.5) * 15;
        
        // Randomly select a color from palette
        const randomColor = colorPalette[Math.floor(Math.random() * colorPalette.length)];
        const brightnessVariation = 0.8 + Math.random() * 0.4; // 0.8-1.2 range
        
        colorArray[i] = randomColor[0] * brightnessVariation;
        colorArray[i+1] = randomColor[1] * brightnessVariation;
        colorArray[i+2] = randomColor[2] * brightnessVariation;
      }
      
      particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
      particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colorArray, 3));
      
      const particlesMaterial = new THREE.PointsMaterial({
        size: 0.04,
        vertexColors: true,
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending,
        sizeAttenuation: true
      });
      
      return new THREE.Points(particlesGeometry, particlesMaterial);
    };

    // Create floating shapes with varied colors
    const createFloatingShapes = () => {
      const shapes = [];
      const geometryTypes = [
        new THREE.IcosahedronGeometry(0.18, 0),
        new THREE.OctahedronGeometry(0.18, 0),
        new THREE.TetrahedronGeometry(0.18, 0),
        new THREE.DodecahedronGeometry(0.15, 0)
      ];
      
      for(let i = 0; i < 15; i++) { // Increased count
        const geometry = geometryTypes[Math.floor(Math.random() * geometryTypes.length)];
        
        // Varied purple hues
        const hue = 0.7 + Math.random() * 0.2; // 0.7-0.9 range (purple)
        const saturation = 0.7 + Math.random() * 0.2;
        const lightness = 0.3 + Math.random() * 0.3;
        
        const color = new THREE.Color().setHSL(hue, saturation, lightness);
        
        const material = new THREE.MeshBasicMaterial({
          color: color,
          transparent: true,
          opacity: 0.5,
          wireframe: true,
          wireframeLinewidth: 1.5
        });
        
        const mesh = new THREE.Mesh(geometry, material);
        
        mesh.position.set(
          (Math.random() - 0.5) * 8,
          (Math.random() - 0.5) * 8,
          (Math.random() - 0.5) * 8
        );
        
        mesh.userData = {
          speed: 0.005 + Math.random() * 0.01,
          direction: new THREE.Vector3(
            Math.random() - 0.5,
            Math.random() - 0.5,
            Math.random() - 0.5
          ).normalize(),
          rotationSpeed: new THREE.Vector3(
            Math.random() * 0.005,
            Math.random() * 0.005,
            Math.random() * 0.005
          )
        };
        
        shapes.push(mesh);
        scene.add(mesh);
      }
      
      return shapes;
    };

    // Create scene elements
    const particlesMesh = createParticles();
    scene.add(particlesMesh);
    
    const floatingShapes = createFloatingShapes();
    
    // Camera position
    camera.position.z = 7;

    // Animation loop
    let animationId;
    const animate = () => {
      animationId = requestAnimationFrame(animate);
      
      // Rotate particles
      particlesMesh.rotation.x += 0.0001;
      particlesMesh.rotation.y += 0.00015;
      
      // Animate floating shapes
      floatingShapes.forEach(shape => {
        shape.position.addScaledVector(shape.userData.direction, shape.userData.speed);
        
        // Bounce in larger space
        if (Math.abs(shape.position.x) > 5) shape.userData.direction.x *= -1;
        if (Math.abs(shape.position.y) > 5) shape.userData.direction.y *= -1;
        if (Math.abs(shape.position.z) > 5) shape.userData.direction.z *= -1;
        
        shape.rotation.x += shape.userData.rotationSpeed.x;
        shape.rotation.y += shape.userData.rotationSpeed.y;
        shape.rotation.z += shape.userData.rotationSpeed.z;
      });
      
      renderer.render(scene, camera);
    };
    
    animationId = requestAnimationFrame(animate);

    // Handle resize
    const handleResize = () => {
      camera.aspect = mount.clientWidth / mount.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(mount.clientWidth, mount.clientHeight);
    };
    
    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationId);
      mount.removeChild(renderer.domElement);
      
      // Dispose all resources
      renderer.dispose();
      particlesMesh.geometry.dispose();
      particlesMesh.material.dispose();
      
      floatingShapes.forEach(shape => {
        shape.geometry.dispose();
        shape.material.dispose();
        scene.remove(shape);
      });
    };
  }, []);

  return (
    <div 
      ref={mountRef} 
      className="three-background" 
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: -1,
        pointerEvents: 'none'
      }} 
    />
  );
};

export default ThreeBackground;