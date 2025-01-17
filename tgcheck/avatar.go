func (tc *TelegramChecker) getUserProfilePhoto(ctx context.Context, u *tg.User, big bool) (string, []byte, error) {
	if u == nil || u.Photo == nil {
	 return "", nil, fmt.Errorf("user is nil or user photo is nil")
	}
	photo := u.Photo.(*tg.UserProfilePhoto)
	fileLocation := &tg.InputPeerPhotoFileLocation{
	 PhotoID: photo.PhotoID,
	 Peer:    &tg.InputPeerUser{UserID: u.ID, AccessHash: u.AccessHash},
	 Big:     big,
	}
   
	sizeFlag := "s"
	if big {
	 sizeFlag = "b"
	}
   
	offset := int64(0)
	limit := int(128 * 1024)
	var photoData []byte
	for {
	 file, err := tc.api.UploadGetFile(ctx, &tg.UploadGetFileRequest{Location: fileLocation, Offset: offset, Limit: limit})
	 if err != nil {
	  return "", nil, fmt.Errorf("failed to get profile photo: %w", err)
	 }
   
	 switch f := file.(type) {
	 case *tg.UploadFile:
	  photoData = append(photoData, f.Bytes...)
	  if len(f.Bytes) < limit {
	   goto Done
	  }
	 case *tg.UploadFileCDNRedirect:
	  return "", nil, fmt.Errorf("CDN files are not supported")
	 default:
	  return "", nil, fmt.Errorf("unexpected response type: %T", file)
	 }
	 offset += int64(limit)
	}
   Done:
	// Detect file extension from mime type
	fileExt := "jpg" // default extension
	if len(photoData) > 0 {
	 // Check magic numbers for common image formats
	 switch {
	 case bytes.HasPrefix(photoData, []byte{0xFF, 0xD8, 0xFF}):
	  fileExt = "jpg"
	 case bytes.HasPrefix(photoData, []byte{0x89, 0x50, 0x4E, 0x47}):
	  fileExt = "png"
	 case bytes.HasPrefix(photoData, []byte{0x47, 0x49, 0x46}):
	  fileExt = "gif"
	 case bytes.HasPrefix(photoData, []byte{0x42, 0x4D}):
	  fileExt = "bmp"
	 case bytes.HasPrefix(photoData, []byte{0x52, 0x49, 0x46, 0x46}):
	  fileExt = "webp"
	 }
	}
   
	if *local {
	 // Save to local filesystem
	 fileName := fmt.Sprintf("%s_%d%s.%s", u.Phone, photo.PhotoID, sizeFlag, fileExt)
	 filePath := filepath.Join(*localPhotoPath, fileName)
	 if err := os.WriteFile(filePath, photoData, 0644); err != nil {
	  return "", nil, fmt.Errorf("failed to save photo locally: %w", err)
	 }
	 return fileName, photoData, nil
	}
	// Save to S3
	awsClient := NewAWSClient(os.Getenv("AWS_REGION"))
	fileName := fmt.Sprintf("%s/%d%s.%s", u.Phone, photo.PhotoID, sizeFlag, fileExt)
	reader := bytes.NewReader(photoData)
	url, err := awsClient.UploadToS3(os.Getenv("AWS_BUCKET"), fileName, reader)
	if err != nil {
	 return "", nil, fmt.Errorf("failed to upload photo to S3: %w", err)
	}
	return url, photoData, nil
   }