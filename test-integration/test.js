import fetch from 'node-fetch';
import fs from 'fs';

async function testWorkflow() {
    console.log('🚀 Starting Integration Test...');
    
    // Test 1: Backend API
    console.log('\n📡 Testing Backend API...');
    try {
        const response = await fetch('http://localhost:8000/api/images/test');
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Backend test endpoint:', data);
        } else {
            console.log('❌ Backend test failed:', response.status);
            return;
        }
    } catch (error) {
        console.log('❌ Backend connection failed:', error.message);
        return;
    }
    
    // Test 2: Image Generation
    console.log('\n🎨 Testing Image Generation...');
    try {
        const response = await fetch('http://localhost:8000/api/images/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: '카페 전단지, 모던한 스타일' })
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Image generation successful');
            console.log(`📏 Image data length: ${data.image_data?.length || 'N/A'}`);
            
            if (data.image_data) {
                // Save the base64 image for verification
                const base64Data = data.image_data;
                const buffer = Buffer.from(base64Data, 'base64');
                fs.writeFileSync('test_output.png', buffer);
                console.log('💾 Test image saved as test_output.png');
            }
        } else {
            console.log('❌ Image generation failed:', response.status);
        }
    } catch (error) {
        console.log('❌ Image generation error:', error.message);
    }
    
    // Test 3: Frontend Status
    console.log('\n🌐 Testing Frontend...');
    try {
        const response = await fetch('http://localhost:5173');
        if (response.ok) {
            console.log('✅ Frontend is accessible');
        } else {
            console.log('❌ Frontend not accessible:', response.status);
        }
    } catch (error) {
        console.log('❌ Frontend connection failed:', error.message);
    }
    
    console.log('\n🏁 Integration test completed!');
    console.log('\n📋 Next Steps:');
    console.log('1. Open http://localhost:5173/flyer-generator in your browser');
    console.log('2. Enter a prompt like "카페 전단지, 모던한 스타일"');
    console.log('3. Click "이미지 생성" button');
    console.log('4. Verify image appears in the canvas');
    console.log('5. Test adding text and shapes');
    console.log('6. Test download functionality');
}

testWorkflow();
