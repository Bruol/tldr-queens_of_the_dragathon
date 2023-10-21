import re

def create_lecture_summary(lecture_title, chunks, summary):
    temp_topics = []
    topics = []


    sections = summary.split("# In-Depth Summaries")

    # Split the summary into sections
    short_topics = sections[0].split("\n## ")
    long_topics = sections[1].split("\n## ")


    # Iterate through each section, skipping the first one (Summary)
    for short_topic in short_topics[1:]:
        topic_title = short_topic.split("\n")[:3][0]

        matches = re.findall(r'Summary (\d+)', short_topic)
        sources = []
        for match in matches:
            for group in match:
                sources.append(group)
        temp = short_topic.split("\n")[3:]
        temp_topics.append((topic_title, '\n'.join(temp), sources))
        
    
    i = 0
    for long_topic in long_topics[1:]:
        long_topic = long_topic.split('\n')[2]
        #long_topic_title = long_topic_lines[0].strip()


        # Add the topic to the topics list
        topics.append((temp_topics[i][0], temp_topics[i][1], long_topic, temp_topics[i][2]))
        i += 1

    # Create the dictionary
    lecture_dict = {
        "lecture_title": lecture_title,
        "chunks": chunks,
        "topics": topics
    }

    return lecture_dict





# Example usage
lecture_title = "Image Analysis, Recognition, and Compression Techniques"
chunks = ["""Summary 1:
This lecture excerpt covers several key topics related to image analysis and recognition. Here is a summary of the main points discussed in the excerpt:

1. **Unitary Transforms and Data Representation**:
   - The lecture begins with an overview of unitary transforms and the representation of data as vectors in high-dimensional vector spaces.
   - Data is stacked together, and the average is subtracted to center the data distribution around zero.

2. **Singular Value Decomposition (SVD)**:
   - The lecturer discusses the use of SVD to identify significant singular values, which capture most of the information in the data.

3. **Rank k Approximation**:
   - The lecture emphasizes the importance of choosing an appropriate rank (k) to approximate the data, with the remaining singular values set to zero.

4. **Challenges in Image Recognition**:
   - Challenges in image recognition include variations in lighting, small shifts in facial features, and noise in high-resolution images.

5. **Eigenfaces**:
   - Eigenfaces are discussed as a method for facial recognition, where faces are represented as linear combinations of eigenfaces.

6. **Handling Illumination Variation**:
   - The lecture points out that for data with changing illumination, it can be better to ignore the first few components of eigenfaces.

7. **Linear Methods for Data Separation**:
   - Linear methods for separating data into classes are introduced, focusing on maximizing the variance within classes while minimizing the variance between classes.

8. **Generalized Eigenvector Problem**:
   - The problem of maximizing within-class variation and minimizing between-class variation can be approached as a generalized eigenvector problem.

9. **PCA vs. Fisher Linear Discriminant**:
   - The lecture demonstrates the differences between Principal Component Analysis (PCA) and Fisher Linear Discriminant in separating data classes. Fisher Linear Discriminant aims to find the direction in which classes are most distinct.

10. **Fisher Faces**:
    - Fisher faces are introduced as a modification of eigenfaces that prioritize the dimensions along which different classes vary the most, leading to better separation.

This excerpt from the lecture covers fundamental concepts in data analysis, dimensionality reduction, and linear methods for classification and recognition, particularly in the context of face recognition.
""", """"Summary 2:
In this lecture transcript excerpt, the speaker discusses the application of Principal Component Analysis (PCA) and Fisher Linear Discriminant (Fisher Faces) to handle data with variations, particularly in the context of lighting conditions. Here's a summary of the key points:

1. **Dimensionality Reduction with PCA**:
   - The speaker begins by explaining the concept of dimensionality reduction. They describe the process of reducing a 2D space to 1D by projecting it onto the dominant principal component.

2. **Projection on Dominant Principal Component**:
   - By conducting Principal Component Analysis (PCA), the dominant principal component is identified, capturing the direction of maximum variation in the data.

3. **Illustration of PCA on Data**:
   - The speaker uses an example with two classes, represented as circles and pluses. The data points initially have good separation based on their classes.
   - However, when PCA is applied, it identifies the direction of maximum variance, which doesn't necessarily align with the direction that separates the classes effectively.

4. **Fisher Linear Discriminant**:
   - The limitations of PCA in terms of class separation are discussed.
   - Fisher Linear Discriminant is introduced as an alternative method that considers both within-class and between-class variations.
   - The goal is to find a direction that maximizes the separation between classes.

5. **Projection with Fisher Faces**:
   - The speaker explains how Fisher Faces, in contrast to PCA, selects a direction that optimally separates classes.
   - When projecting data onto this direction, it results in a better separation of classes, effectively improving classification.

6. **Handling Lighting Variation**:
   - The lecture touches upon the influence of lighting conditions on data.
   - It is noted that lighting conditions can be well-modeled using the first three principal components.
   - This is based on the physics of how light interacts with surfaces, considering the surface normals and light direction.

7. **Illustration of Data Distribution**:
   - The speaker uses a data distribution with a circular shape to contrast with the previous linear data distribution.

8. **Addressing Circular Data Distribution**:
   - The challenges of handling circular data distributions are briefly mentioned.
   - The speaker doesn't delve into the solution but introduces the idea that different data distributions may require unique approaches.

9. **Example Applications**:
   - The lecture highlights the practical applications of these techniques, such as recognizing faces with or without glasses, where Fisher Faces outperforms Eigen Faces.

The excerpt provides insights into dimensionality reduction techniques like PCA and Fisher Linear Discriminant and their application to image analysis, with a particular focus on improving face recognition under various conditions, especially lighting variations.
""", """"Summary 3:
In this lecture transcript excerpt, the speaker discusses image compression techniques and the principles of JPEG compression. Here is a summary of the main points:

- The speaker explains a method for identifying and classifying objects, particularly faces, using techniques like principal component analysis and Fisher linear discriminant.
- He emphasizes that in some cases, simple linear models are not sufficient to represent the variation in data, and more complex models are required to account for nonlinearities.
- The speaker introduces an example of analyzing the appearance of objects under various viewpoints and how it can be represented using principal component analysis.
- He mentions how some objects may have multiple variations and how the analysis can capture these variations.
- The speaker transitions to discussing image compression and the use of principal component analysis for compressing natural images.
- He shows that natural images exhibit more low-frequency content and that human vision is less sensitive to high frequencies.
- The use of the discrete cosine transform for image compression is introduced, and its basis functions are discussed.
- The quantization step, which involves dividing the coefficients by a quantization matrix, is briefly mentioned as part of the JPEG compression process.

The lecture excerpt primarily focuses on techniques for analyzing and compressing images, particularly in the context of the JPEG compression standard.
""", """"Summary 4:
This lecture excerpt discusses the use of the Discrete Cosine Transform (DCT) in JPEG image compression. Here's a summary of the key points:

- **DCT Overview**: The lecturer explains that DCT is a mathematical transformation used in JPEG compression. It's closely related to the Fourier transform but deals with strictly real numbers. DCT is used to transform an 8x8 block of pixel values into 64 coefficients with respect to specific basis functions.

- **Quantization**: To reduce the amount of data, quantization is applied after the DCT. A quantization matrix is used to divide the coefficients, resulting in fewer bits being allocated to higher frequency components. This step introduces loss into the compression process.

- **Zigzag Scanning**: The lecturer describes the zigzag scan, a method to encode the quantized coefficients efficiently. By zigzagging through the coefficients, a point is reached where most of the coefficients become zero. The rest of the coefficients are encoded, and the rest are ignored.

- **Lossy and Lossless Compression**: JPEG compression involves both lossy and lossless components. The quantization step introduces loss, as it discards some data. Additionally, entropy coding, such as Huffman coding, is used for further lossless compression.

- **Scale Spaces**: The lecture briefly mentions the concept of scale spaces, highlighting the importance of representing images at various scales. Different scales capture varying levels of detail, which can be useful in tasks like matching features and edge detection.

- **Neural Networks in Face Detection**: The lecture concludes with an example of using neural networks for face detection. In this example, a neural network analyzes a fixed-size region (20x20 pixels) to determine the presence of a face. The challenge is to apply this network at different resolutions within an image to detect faces of various sizes.

Overall, the lecture provides an overview of how JPEG compression works, focusing on the DCT, quantization, and other key techniques involved in this image compression standard.
""", """"Summary 5;
In this lecture excerpt, the speaker discusses the use of wavelet transforms in image processing and how they differ from other methods like the discrete cosine transform (DCT) used in JPEG compression. Here are the key points:

1. **CMU Face Detector:** The lecture begins by mentioning an example of the CMU face detector, an older system that utilized neural networks for face detection around 20 years ago. This system used neural networks to identify patterns of faces within fixed-size image templates.

2. **Scale-Space Representations:** The lecture delves into the concept of scale-space representations. These representations involve capturing patterns at different scales or resolutions within an image. The goal is to maintain the quality of features and their locations as the image's scale changes. One common technique to achieve this is the use of image pyramids, which progressively reduce the image resolution to capture information at different scales.

3. **Wavelet Transforms:** The lecture introduces wavelet transforms as a method that provides both spatial and frequency locality. This is in contrast to the Fourier transform, which is global in frequency. Wavelet transforms involve the use of a filter bank, including low-pass and high-pass filters, to capture different scales and locations in the image.

4. **Hart Wavelet Basis:** The speaker provides an example of the Hart wavelet basis, illustrating how it differs from the DCT used in JPEG compression. The Hart basis is localized both in terms of frequency and location, allowing it to represent signals in a more compact manner.

5. **Wavelet Transform Construction:** The lecture explains how wavelet transforms can be constructed, involving a series of filtering and subsampling steps to separate and capture various scales within the image. The key point is that subsampling high-frequency components is not an issue because the representation primarily consists of high-frequency information.

Overall, this excerpt provides insights into the use of wavelet transforms and their advantages in representing signals with both spatial and frequency locality, which can be valuable in image processing tasks.
""", """Summary 6:
In this lecture transcript excerpt, the speaker discusses the application of wavelet transforms, specifically Hart wavelet transforms, in image compression. Here are the key points:

1. **Wavelet Transform Construction:** The speaker explains the process of applying wavelet transforms to an image. This involves a series of steps, including upsampling, filtering, and splitting the low-pass and high-pass components of the image. The goal is to decompose the image into various frequency components.

2. **Aliasing and Decomposition:** The speaker addresses the issue of subsampling high-frequency components and the potential for aliasing. However, in the context of wavelet transforms, aliasing is not problematic because it only affects high-frequency components. The speaker emphasizes that knowing the frequency band of the signal prevents confusion.

3. **Wavelet Decomposition of an Image:** The lecture provides an example of wavelet decomposition of an image, showing how the low-frequency and high-frequency components are separated and reconstructed. The speaker highlights that the wavelet decomposition reveals regions of similar frequency content in the image.

4. **Biorthogonal Perfect Reconstruction:** The speaker mentions the concept of biorthogonal perfect reconstruction, where a combination of four filters is used to achieve a perfect reconstruction of the signal. This method allows for the use of short, finite filters.

5. **JPEG 2000 and Image Compression:** The lecture briefly mentions the use of wavelet compression in JPEG 2000, a standard for image compression. It contrasts the quality of reconstruction between standard JPEG and JPEG 2000, highlighting the superior quality of JPEG 2000.

6. **Use of Wavelets in Video Compression:** The lecture hints at the upcoming topic of optical flow and its application in video compression. Optical flow is introduced as a method for determining the motion of visual patterns in video, and it will be discussed in the next lecture.

The lecture concludes with a preview of the next topics, optical flow, and how optical flow can be combined with image compression techniques to efficiently encode videos."""]
summary = """# Summary

## Image Analysis and Recognition

### Sourced from Summary 1 and Summary 4
- **Unitary Transforms and Data Representation**:
   - Data is represented as vectors in high-dimensional spaces.
   - Centering data distribution around zero.
   
- **Singular Value Decomposition (SVD)**:
   - Identifying significant singular values to capture data information.

- **Linear Methods for Data Separation**:
   - Maximizing within-class variance, minimizing between-class variance.

- **PCA vs. Fisher Linear Discriminant**:
   - Comparing Principal Component Analysis (PCA) and Fisher Linear Discriminant for data separation.

## Dimensionality Reduction and Face Recognition

### Sourced from Summary 2
- **Dimensionality Reduction with PCA**:
   - Reducing data to lower dimensions.
   - Projecting data onto the dominant principal component.

- **Fisher Linear Discriminant**:
   - Maximizing class separation.

- **Handling Lighting Variation**:
   - Modeling lighting with principal components.
   
## Image Compression and JPEG

### Sourced from Summary 3
- **JPEG Compression Principles**:
   - Overview of JPEG image compression.
   - DCT, quantization, and entropy coding in JPEG.
   
## Discrete Cosine Transform (DCT) in JPEG

### Sourced from Summary 4
- **DCT Overview**:
   - Role of Discrete Cosine Transform in JPEG.
   
- **Quantization**:
   - Reducing data through quantization.
   
- **Zigzag Scanning**:
   - Efficient encoding of quantized coefficients.

## Wavelet Transforms in Image Processing

### Sourced from Summary 5
- **Scale-Space Representations**:
   - Capturing patterns at different scales.

- **Wavelet Transforms**:
   - Providing spatial and frequency locality.
   
## Hart Wavelet Transforms in Image Compression

### Sourced from Summary 6
- **Wavelet Transform Construction**:
   - Decomposing images into frequency components.
   
- **Aliasing and Decomposition**:
   - Addressing aliasing in wavelet transforms.
   
- **Biorthogonal Perfect Reconstruction**:
   - Achieving perfect signal reconstruction.
   
- **Use of Wavelets in Video Compression**:
   - Combining wavelets with optical flow for video compression.

# In-Depth Summaries

## Image Analysis and Recognition

This section explores the fundamental concepts of image analysis and recognition. It begins with an introduction to unitary transforms and data representation, emphasizing the centering of data distribution around zero. The lecture discusses the significance of Singular Value Decomposition (SVD) in capturing data information and the rank k approximation for dimensionality reduction. It addresses challenges in image recognition, such as lighting variations, small feature shifts, and noise. Eigenfaces, a method for facial recognition, is introduced, along with strategies for handling illumination variation. The lecture further delves into linear methods for separating data classes, culminating in the comparison between Principal Component Analysis (PCA) and Fisher Linear Discriminant. Fisher faces, which prioritize class separability, are presented as an enhancement to eigenfaces.

## Dimensionality Reduction and Face Recognition

This segment delves into dimensionality reduction techniques like Principal Component Analysis (PCA) and Fisher Linear Discriminant (Fisher Faces) in the context of face recognition. It explains how PCA projects data onto the dominant principal component, illustrating its limitations in effectively separating classes. The lecture introduces Fisher Linear Discriminant as a method that maximizes class separation. Handling variations in lighting conditions, particularly using the first three principal components, is discussed. Practical applications of these techniques, such as recognizing faces with and without glasses, are highlighted.

## Image Compression and JPEG

This section provides insights into image compression techniques and the principles of JPEG compression. It discusses the role of Discrete Cosine Transform (DCT) in JPEG compression and the quantization step that introduces loss into the compression process. The concept of zigzag scanning for efficient encoding and the combination of lossy and lossless compression in JPEG are explained. The lecture also touches on the importance of representing images at various scales, using scale spaces.

## Discrete Cosine Transform (DCT) in JPEG

This part of the lecture offers an in-depth look at the Discrete Cosine Transform (DCT) in JPEG image compression. It explains how DCT transforms an 8x8 block of pixel values into coefficients using specific basis functions. The quantization process is described, which reduces data and introduces loss. Zigzag scanning is presented as an efficient encoding method. The lecture highlights the combination of lossy and lossless compression in JPEG and briefly mentions the concept of scale spaces.

## Wavelet Transforms in Image Processing

This section explores the use of wavelet transforms in image processing, particularly in contrast to other methods like the Discrete Cosine Transform (DCT). It starts by referencing the CMU face detector as an early example of using neural networks for face detection. It introduces the concept of scale-space representations, emphasizing the need to capture patterns at different scales in images. Wavelet transforms are presented as a method with both spatial and frequency locality, in contrast to the global frequency representation of the Fourier transform. The lecture provides an example of the Hart wavelet basis and discusses its advantages. It highlights the construction of wavelet transforms through filtering and subsampling, addressing the issue of subsampling high-frequency components and the potential for aliasing.

## Hart Wavelet Transforms in Image Compression

This part of the lecture focuses on the application of Hart wavelet transforms in image compression. It explains the process of constructing wavelet transforms, which involves various steps to decompose images into different frequency components. The lecture addresses aliasing and the decomposition of images, emphasizing that aliasing primarily affects high-frequency components. The concept of biorthogonal perfect reconstruction is introduced, allowing for efficient signal reconstruction. The use of wavelets in image compression standards like JPEG 2000 is briefly mentioned. The lecture concludes with a preview of the next topic, optical flow, and its application in video compression.
"""

result = create_lecture_summary(lecture_title, chunks, summary)
print(type(result["topics"][0]))
print(result["topics"][0][0])
print(result["topics"][0][1])
print(result["topics"][0][2])
print(result["topics"][0][3])
