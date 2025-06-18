import baseApiUrl from "./baseUrl";

interface CourseImage {
  itemImageSrc: string,
  thumbnailImageSrc?: string,
  alt: string,
  title: string
}

export const PhotoService = {
  getData(): CourseImage[] {
    return [
      {
        itemImageSrc: new URL("/get_file/media/image/test_image.jpg", baseApiUrl).toString(),
        thumbnailImageSrc:
          'https://primefaces.org/cdn/primevue/images/galleria/galleria1s.jpg',
        alt: 'Description for Image 1',
        title: 'Title 1',
      },
      {
        itemImageSrc: new URL("/get_file/media/image/test_image.jpg", baseApiUrl).toString(),
        alt: 'Description for Image 1',
        title: 'Title 1',
      },
    ];
  },

  getImages(): Promise<CourseImage[]> {
    return Promise.resolve(this.getData());
  },
};
